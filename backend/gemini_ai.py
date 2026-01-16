"""
Gemini AI Integration - Intelligent Android Code Generation
"""
import requests
import json

class GeminiAI:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def generate_app_concept(self, idea):
        """Generate detailed app concept from user idea"""
        
        prompt = f"""You are an expert Android app architect. Analyze this app idea and provide a detailed concept:

Idea: {idea}

Provide a JSON response with:
{{
    "app_name": "unique app name",
    "category": "ecommerce/social/health/productivity/news",
    "description": "detailed description",
    "unique_features": ["feature 1", "feature 2", "feature 3"],
    "color_scheme": "primary color suggestion",
    "target_audience": "who will use this",
    "key_screens": ["screen 1", "screen 2"]
}}"""
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                
                # Extract JSON from response
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end > start:
                    return json.loads(text[start:end])
            
            return None
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    def generate_screen_content(self, app_name, screen_name, category):
        """Generate content for a specific screen"""
        
        prompt = f"""Generate realistic content for this Android app screen:

App: {app_name}
Category: {category}
Screen: {screen_name}

Provide 3-5 realistic data items that would appear on this screen. Keep it simple and professional.
Return as JSON array: ["item 1", "item 2", "item 3"]"""
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                
                start = text.find('[')
                end = text.rfind(']') + 1
                if start != -1 and end > start:
                    return json.loads(text[start:end])
            
            return ["Sample Item 1", "Sample Item 2", "Sample Item 3"]
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return ["Sample Item 1", "Sample Item 2", "Sample Item 3"]
