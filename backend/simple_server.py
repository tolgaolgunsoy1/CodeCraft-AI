from flask import Flask, jsonify, send_from_directory, request, send_file
from flask_cors import CORS
import time
import uuid
import os
import zipfile
import tempfile

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

project_storage = {}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/enterprise.html')
def enterprise():
    return send_from_directory(app.static_folder, 'final_enterprise.html')

@app.route('/config_panel.html')
def config_panel():
    return send_from_directory(app.static_folder, 'config_panel.html')

@app.route('/api/generate-app', methods=['POST'])
def generate_app():
    """Real Android project generation"""
    data = request.get_json()
    idea = data.get('idea', 'My App')
    architecture = data.get('architecture', 'single_activity')
    ui_framework = data.get('uiFramework', 'xml')
    
    # Import the real generator
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from android_generator import AndroidAppGenerator
    
    try:
        # Create real Android project
        generator = AndroidAppGenerator()
        project_id = str(uuid.uuid4())
        app_name = idea.split()[0].capitalize() + 'App'
        
        # Generate real project
        result = generator.generate_from_idea(
            idea=idea,
            language='java',
            architecture=architecture,
            ui_framework=ui_framework,
            project_path=None,
            app_name=app_name
        )
        
        project_path = result['project_path']
        
        # Store project info
        project_storage[project_id] = {
            'appName': app_name,
            'idea': idea,
            'architecture': architecture,
            'uiFramework': ui_framework,
            'projectPath': project_path,
            'created_at': time.time()
        }
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'result': {
                'appName': app_name,
                'description': idea,
                'features': [
                    'Modern Material Design 3',
                    f'{architecture.replace("_", " ").title()} Architecture',
                    f'{ui_framework.upper()} UI Framework',
                    'Firebase Backend Integration',
                    'Retrofit API Client',
                    'Room Database',
                    'Dark Mode Support',
                    'Multi-language Support'
                ],
                'projectPath': project_path,
                'screens': [
                    'SplashActivity - Açılış ekranı',
                    'MainActivity - Ana ekran',
                    'ProfileActivity - Kullanıcı profili',
                    'SettingsActivity - Ayarlar'
                ],
                'permissions': [
                    'INTERNET - İnternet erişimi',
                    'ACCESS_NETWORK_STATE - Ağ durumu',
                    'CAMERA - Kamera erişimi'
                ],
                'dependencies': [
                    'androidx.appcompat:appcompat:1.6.1',
                    'com.google.android.material:material:1.11.0',
                    'androidx.constraintlayout:constraintlayout:2.1.4',
                    'com.squareup.retrofit2:retrofit:2.9.0'
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<project_id>')
def download_project(project_id):
    """Generate and download real ZIP file"""
    if project_id not in project_storage:
        return jsonify({'error': 'Project not found'}), 404
    
    project = project_storage[project_id]
    project_path = project.get('projectPath')
    app_name = project['appName']
    
    if not project_path or not os.path.exists(project_path):
        return jsonify({'error': 'Project files not found'}), 404
    
    # Create ZIP from real project
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, f"{app_name}.zip")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all project files
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, os.path.dirname(project_path))
                    zipf.write(file_path, arc_name)
        
        return send_file(zip_path, as_attachment=True, download_name=f"{app_name}.zip")
        
    except Exception as e:
        return jsonify({'error': f'Failed to create ZIP: {str(e)}'}), 500

if __name__ == '__main__':
    print("Simple Test Backend Starting...")
    print("http://localhost:5000")
    print("http://localhost:5000/enterprise.html")
    app.run(debug=True, host='127.0.0.1', port=5000)
