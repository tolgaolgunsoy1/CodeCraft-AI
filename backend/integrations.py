"""
API Integrations Module
Robust integrations with external services for enhanced functionality
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from functools import lru_cache
import time

logger = logging.getLogger(__name__)

class APIClient:
    """Base API client with retry logic and error handling"""

    def __init__(self, base_url: str, timeout: int = 30, retries: int = 3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"API request failed (attempt {attempt + 1}/{self.retries}): {str(e)}")
                if attempt == self.retries - 1:
                    logger.error(f"API request failed after {self.retries} attempts: {str(e)}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff

        return None

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any] = None, json_data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('POST', endpoint, json=json_data, data=data)

    def put(self, endpoint: str, data: Dict[str, Any] = None, json_data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        return self._make_request('PUT', endpoint, json=json_data, data=data)

    def delete(self, endpoint: str) -> Optional[Dict[str, Any]]:
        return self._make_request('DELETE', endpoint)

class FirebaseService:
    """Firebase integration for real-time features and analytics"""

    def __init__(self, project_id: str = None, credentials_path: str = None):
        self.project_id = project_id or os.getenv('FIREBASE_PROJECT_ID')
        self.credentials_path = credentials_path

        if self.project_id:
            try:
                import firebase_admin
                from firebase_admin import credentials, firestore, messaging

                if not firebase_admin._apps:
                    if self.credentials_path and os.path.exists(self.credentials_path):
                        cred = credentials.Certificate(self.credentials_path)
                    else:
                        cred = credentials.ApplicationDefault()

                    firebase_admin.initialize_app(cred, {
                        'projectId': self.project_id
                    })

                self.firestore = firestore.client()
                self.messaging = messaging
                self.initialized = True
                logger.info("Firebase initialized successfully")
            except ImportError:
                logger.warning("Firebase SDK not available")
                self.initialized = False
            except Exception as e:
                logger.error(f"Firebase initialization failed: {str(e)}")
                self.initialized = False
        else:
            self.initialized = False
            logger.warning("Firebase project ID not configured")

    def log_event(self, user_id: str, event_name: str, parameters: Dict[str, Any] = None) -> bool:
        """Log analytics event"""
        if not self.initialized:
            return False

        try:
            doc_ref = self.firestore.collection('analytics_events').document()
            doc_ref.set({
                'user_id': user_id,
                'event_name': event_name,
                'parameters': parameters or {},
                'timestamp': datetime.utcnow()
            })
            return True
        except Exception as e:
            logger.error(f"Failed to log Firebase event: {str(e)}")
            return False

    def send_push_notification(self, token: str, title: str, body: str, data: Dict[str, Any] = None) -> bool:
        """Send push notification"""
        if not self.initialized:
            return False

        try:
            message = self.messaging.Message(
                notification=self.messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token
            )
            self.messaging.send(message)
            return True
        except Exception as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return False

    def store_user_data(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Store user data in Firestore"""
        if not self.initialized:
            return False

        try:
            doc_ref = self.firestore.collection('users').document(user_id)
            doc_ref.set(data, merge=True)
            return True
        except Exception as e:
            logger.error(f"Failed to store user data: {str(e)}")
            return False

class StripeService:
    """Stripe integration for payment processing"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('STRIPE_SECRET_KEY')

        if self.api_key:
            try:
                import stripe
                stripe.api_key = self.api_key
                self.stripe = stripe
                self.initialized = True
                logger.info("Stripe initialized successfully")
            except ImportError:
                logger.warning("Stripe SDK not available")
                self.initialized = False
            except Exception as e:
                logger.error(f"Stripe initialization failed: {str(e)}")
                self.initialized = False
        else:
            self.initialized = False
            logger.warning("Stripe API key not configured")

    def create_payment_intent(self, amount: int, currency: str = 'usd',
                             metadata: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Create payment intent"""
        if not self.initialized:
            return None

        try:
            intent = self.stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True}
            )
            return {
                'id': intent.id,
                'client_secret': intent.client_secret,
                'amount': intent.amount,
                'currency': intent.currency
            }
        except Exception as e:
            logger.error(f"Failed to create payment intent: {str(e)}")
            return None

    def confirm_payment(self, payment_intent_id: str) -> bool:
        """Confirm payment intent"""
        if not self.initialized:
            return False

        try:
            intent = self.stripe.PaymentIntent.confirm(payment_intent_id)
            return intent.status == 'succeeded'
        except Exception as e:
            logger.error(f"Failed to confirm payment: {str(e)}")
            return False

    def create_subscription(self, customer_id: str, price_id: str) -> Optional[Dict[str, Any]]:
        """Create subscription"""
        if not self.initialized:
            return None

        try:
            subscription = self.stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent']
            )
            return {
                'id': subscription.id,
                'status': subscription.status,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret
            }
        except Exception as e:
            logger.error(f"Failed to create subscription: {str(e)}")
            return None

class GoogleAnalyticsService:
    """Google Analytics integration"""

    def __init__(self, tracking_id: str = None):
        self.tracking_id = tracking_id or os.getenv('GOOGLE_ANALYTICS_ID')
        self.initialized = bool(self.tracking_id)

        if self.initialized:
            logger.info("Google Analytics initialized")
        else:
            logger.warning("Google Analytics tracking ID not configured")

    def track_event(self, category: str, action: str, label: str = None, value: int = None) -> bool:
        """Track event (placeholder for actual GA implementation)"""
        if not self.initialized:
            return False

        # In a real implementation, this would send data to Google Analytics
        logger.info(f"GA Event: {category} - {action} - {label} - {value}")
        return True

    def track_pageview(self, page_path: str, page_title: str = None) -> bool:
        """Track page view"""
        if not self.initialized:
            return False

        logger.info(f"GA Pageview: {page_path} - {page_title}")
        return True

class OpenAIService:
    """OpenAI integration for AI-powered features"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"

        if self.api_key:
            self.client = APIClient(self.base_url)
            self.client.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
            self.initialized = True
            logger.info("OpenAI service initialized")
        else:
            self.initialized = False
            logger.warning("OpenAI API key not configured")

    def generate_app_description(self, app_idea: str) -> Optional[str]:
        """Generate app description using AI"""
        if not self.initialized:
            return None

        prompt = f"""
        Generate a compelling app description for the following idea:
        "{app_idea}"

        Make it engaging, highlight key features, and keep it under 200 characters.
        """

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150,
            'temperature': 0.7
        }

        response = self.client.post('chat/completions', json_data=data)
        if response and 'choices' in response:
            return response['choices'][0]['message']['content'].strip()

        return None

    def suggest_features(self, app_idea: str, category: str) -> List[str]:
        """Suggest features for the app"""
        if not self.initialized:
            return []

        prompt = f"""
        Suggest 5-7 key features for a {category} app with the following idea:
        "{app_idea}"

        Return as a JSON array of feature descriptions.
        """

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 300,
            'temperature': 0.7
        }

        response = self.client.post('chat/completions', json_data=data)
        if response and 'choices' in response:
            try:
                content = response['choices'][0]['message']['content'].strip()
                # Try to parse as JSON
                features = json.loads(content)
                if isinstance(features, list):
                    return features
            except json.JSONDecodeError:
                # Fallback: split by newlines
                return [line.strip('- ').strip() for line in content.split('\n') if line.strip()]

        return []

class GitHubService:
    """GitHub integration for code hosting and collaboration"""

    def __init__(self, token: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"

        if self.token:
            self.client = APIClient(self.base_url)
            self.client.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
            self.initialized = True
            logger.info("GitHub service initialized")
        else:
            self.initialized = False
            logger.warning("GitHub token not configured")

    def create_repository(self, name: str, description: str = "", private: bool = False) -> Optional[Dict[str, Any]]:
        """Create a new GitHub repository"""
        if not self.initialized:
            return None

        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': True
        }

        response = self.client.post('user/repos', json_data=data)
        return response

    def upload_file(self, repo_owner: str, repo_name: str, file_path: str, content: str, message: str) -> bool:
        """Upload file to repository"""
        if not self.initialized:
            return False

        # First, get the file SHA if it exists
        sha = None
        get_response = self.client.get(f'repos/{repo_owner}/{repo_name}/contents/{file_path}')
        if get_response and 'sha' in get_response:
            sha = get_response['sha']

        data = {
            'message': message,
            'content': content.encode('utf-8').decode('latin1'),  # GitHub expects latin1
            'branch': 'main'
        }

        if sha:
            data['sha'] = sha

        response = self.client.put(f'repos/{repo_owner}/{repo_name}/contents/{file_path}', json_data=data)
        return response is not None

class EmailService:
    """Email service for notifications and communications"""

    def __init__(self, smtp_server: str = None, smtp_port: int = 587,
                 username: str = None, password: str = None):
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port
        self.username = username or os.getenv('SMTP_USERNAME')
        self.password = password or os.getenv('SMTP_PASSWORD')
        self.initialized = all([self.smtp_server, self.username, self.password])

        if self.initialized:
            logger.info("Email service initialized")
        else:
            logger.warning("Email service not fully configured")

    def send_email(self, to_email: str, subject: str, body: str, html_body: str = None) -> bool:
        """Send email"""
        if not self.initialized:
            return False

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email

            # Plain text version
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)

            # HTML version if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())
            server.quit()

            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

# Global service instances
firebase_service = FirebaseService()
stripe_service = StripeService()
analytics_service = GoogleAnalyticsService()
openai_service = OpenAIService()
github_service = GitHubService()
email_service = EmailService()

# Utility functions
@lru_cache(maxsize=100)
def get_cached_api_response(url: str, params: str = "") -> Optional[Dict[str, Any]]:
    """Cache API responses to reduce external calls"""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Cached API request failed: {str(e)}")
        return None

def health_check_services() -> Dict[str, bool]:
    """Check health of all integrated services"""
    services_status = {
        'firebase': firebase_service.initialized,
        'stripe': stripe_service.initialized,
        'analytics': analytics_service.initialized,
        'openai': openai_service.initialized,
        'github': github_service.initialized,
        'email': email_service.initialized
    }

    logger.info(f"Service health check: {services_status}")
    return services_status