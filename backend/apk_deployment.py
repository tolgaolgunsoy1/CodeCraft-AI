# Automatic APK Deployment - One-Click Phone Installation

import qrcode
import io
import base64
from flask import send_file, jsonify
import os
import subprocess
import threading

class APKDeploymentSystem:
    """Automatic APK deployment to phone"""
    
    @staticmethod
    def generate_qr_code(apk_url: str) -> str:
        """Generate QR code for APK download"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(apk_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def build_apk_cloud(project_path: str) -> dict:
        """Build APK on server (cloud build)"""
        try:
            # Run Gradle build
            result = subprocess.run(
                ['./gradlew', 'assembleDebug'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                apk_path = os.path.join(
                    project_path, 
                    'app/build/outputs/apk/debug/app-debug.apk'
                )
                
                if os.path.exists(apk_path):
                    return {
                        'success': True,
                        'apk_path': apk_path,
                        'size': os.path.getsize(apk_path) / (1024 * 1024),  # MB
                        'message': 'APK built successfully'
                    }
            
            return {
                'success': False,
                'error': result.stderr
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def send_to_phone_via_adb(apk_path: str) -> dict:
        """Send APK to phone via ADB (USB debugging)"""
        try:
            # Check if device connected
            check = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True
            )
            
            if 'device' not in check.stdout:
                return {
                    'success': False,
                    'error': 'No device connected. Enable USB debugging.'
                }
            
            # Install APK
            result = subprocess.run(
                ['adb', 'install', '-r', apk_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'APK installed on phone successfully!'
                }
            
            return {
                'success': False,
                'error': result.stderr
            }
            
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'ADB not found. Install Android SDK Platform Tools.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def create_download_page(apk_url: str, qr_code: str, app_name: str) -> str:
        """Create mobile-friendly download page"""
        return f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - İndir</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }}
        
        .icon {{
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 25px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
        }}
        
        h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}
        
        .qr-code {{
            margin: 30px 0;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 15px;
        }}
        
        .qr-code img {{
            max-width: 250px;
            width: 100%;
        }}
        
        .download-btn {{
            display: block;
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            transition: transform 0.2s;
        }}
        
        .download-btn:active {{
            transform: scale(0.98);
        }}
        
        .info {{
            background: #f0f9ff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
            color: #0369a1;
        }}
        
        .steps {{
            text-align: left;
            margin-top: 20px;
            padding: 20px;
            background: #fef3c7;
            border-radius: 10px;
        }}
        
        .steps h3 {{
            font-size: 16px;
            margin-bottom: 10px;
            color: #92400e;
        }}
        
        .steps ol {{
            margin-left: 20px;
            color: #78350f;
        }}
        
        .steps li {{
            margin-bottom: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📱</div>
        <h1>{app_name}</h1>
        <p class="subtitle">Uygulamanız hazır!</p>
        
        <a href="{apk_url}" class="download-btn" download>
            📥 APK İndir (Direkt)
        </a>
        
        <div class="qr-code">
            <p style="margin-bottom: 10px; color: #666;">veya QR Kod ile:</p>
            <img src="{qr_code}" alt="QR Code">
        </div>
        
        <div class="info">
            ℹ️ APK boyutu: ~14 MB<br>
            Android 7.0+ gereklidir
        </div>
        
        <div class="steps">
            <h3>📋 Kurulum Adımları:</h3>
            <ol>
                <li>APK dosyasını indirin</li>
                <li>"Bilinmeyen kaynaklara izin ver" seçeneğini aktif edin</li>
                <li>APK dosyasına tıklayın</li>
                <li>"Yükle" butonuna basın</li>
                <li>Uygulama ana ekranınızda hazır! 🎉</li>
            </ol>
        </div>
    </div>
    
    <script>
        // Auto-download on mobile
        if (/Android/i.test(navigator.userAgent)) {{
            setTimeout(() => {{
                if (confirm('APK dosyasını şimdi indirmek ister misiniz?')) {{
                    window.location.href = '{apk_url}';
                }}
            }}, 1000);
        }}
    </script>
</body>
</html>'''


# Flask endpoints for deployment
def setup_deployment_routes(app, project_storage_path):
    """Setup Flask routes for APK deployment"""
    
    @app.route('/api/build-apk/<project_id>', methods=['POST'])
    def build_apk(project_id):
        """Build APK on server"""
        project_path = os.path.join(project_storage_path, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Build in background
        def build_async():
            result = APKDeploymentSystem.build_apk_cloud(project_path)
            # Store result for later retrieval
            
        thread = threading.Thread(target=build_async, daemon=True)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'APK build started',
            'estimated_time': '2-3 minutes'
        })
    
    @app.route('/api/install-phone/<project_id>', methods=['POST'])
    def install_to_phone(project_id):
        """Install APK to connected phone via ADB"""
        apk_path = os.path.join(
            project_storage_path, 
            project_id, 
            'app/build/outputs/apk/debug/app-debug.apk'
        )
        
        if not os.path.exists(apk_path):
            return jsonify({
                'success': False, 
                'error': 'APK not found. Build first.'
            }), 404
        
        result = APKDeploymentSystem.send_to_phone_via_adb(apk_path)
        return jsonify(result)
    
    @app.route('/download/<project_id>')
    def download_page(project_id):
        """Mobile-friendly download page"""
        apk_url = f"/api/download-apk/{project_id}"
        qr_code = APKDeploymentSystem.generate_qr_code(
            f"http://{request.host}{apk_url}"
        )
        
        html = APKDeploymentSystem.create_download_page(
            apk_url=apk_url,
            qr_code=qr_code,
            app_name=project_id
        )
        
        return html
    
    @app.route('/api/download-apk/<project_id>')
    def download_apk(project_id):
        """Direct APK download"""
        apk_path = os.path.join(
            project_storage_path,
            project_id,
            'app/build/outputs/apk/debug/app-debug.apk'
        )
        
        if not os.path.exists(apk_path):
            return jsonify({'error': 'APK not found'}), 404
        
        return send_file(
            apk_path,
            as_attachment=True,
            download_name=f'{project_id}.apk',
            mimetype='application/vnd.android.package-archive'
        )


# Frontend JavaScript for deployment
DEPLOYMENT_JS = '''
// APK Deployment Functions

async function buildAndDownload(projectId) {
    try {
        // Show loading
        showLoading('APK oluşturuluyor...');
        
        // Start build
        const buildResponse = await fetch(`/api/build-apk/${projectId}`, {
            method: 'POST'
        });
        
        const buildResult = await buildResponse.json();
        
        if (buildResult.success) {
            // Poll for completion
            await pollBuildStatus(projectId);
            
            // Show download options
            showDownloadOptions(projectId);
        } else {
            showError(buildResult.error);
        }
    } catch (error) {
        showError('APK oluşturma hatası: ' + error.message);
    }
}

async function pollBuildStatus(projectId) {
    return new Promise((resolve) => {
        const interval = setInterval(async () => {
            const response = await fetch(`/api/build-status/${projectId}`);
            const result = await response.json();
            
            if (result.status === 'completed') {
                clearInterval(interval);
                resolve();
            }
        }, 2000);
    });
}

function showDownloadOptions(projectId) {
    const modal = document.createElement('div');
    modal.className = 'download-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>🎉 APK Hazır!</h2>
            <p>Uygulamanızı telefonunuza yükleyin:</p>
            
            <div class="download-options">
                <button onclick="downloadDirect('${projectId}')" class="btn-primary">
                    📥 Direkt İndir
                </button>
                
                <button onclick="showQRCode('${projectId}')" class="btn-secondary">
                    📱 QR Kod ile İndir
                </button>
                
                <button onclick="installViaADB('${projectId}')" class="btn-secondary">
                    🔌 USB ile Yükle (ADB)
                </button>
            </div>
            
            <div class="info-box">
                ℹ️ <strong>İpucu:</strong> QR kodu telefonunuzla tarayın ve direkt indirin!
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function downloadDirect(projectId) {
    window.open(`/download/${projectId}`, '_blank');
}

function showQRCode(projectId) {
    window.open(`/download/${projectId}`, '_blank');
}

async function installViaADB(projectId) {
    try {
        showLoading('Telefona yükleniyor...');
        
        const response = await fetch(`/api/install-phone/${projectId}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess('✅ Uygulama telefonunuza yüklendi!');
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Yükleme hatası: ' + error.message);
    }
}
'''

# Add to requirements.txt
REQUIREMENTS_ADDITION = '''
# APK Deployment
qrcode==7.4.2
Pillow==10.1.0
'''
