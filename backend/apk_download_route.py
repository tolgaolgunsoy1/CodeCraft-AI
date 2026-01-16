@app.route('/download-apk/<project_id>')
@handle_errors
def download_apk(project_id):
    """Download APK file for completed project"""
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        download_id = result.get('downloadId', project_id)
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, download_id)
    else:
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, project_id)

    apk_path = os.path.join(project_path, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
    
    if not os.path.exists(apk_path):
        return jsonify({'success': False, 'error': 'APK dosyası bulunamadı'}), 404
    
    # Get app name for download filename
    app_name = "App"
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        app_name = result.get('appName', 'App')

    # Sanitize app name for filename
    safe_filename = ''.join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_filename:
        safe_filename = "App"

    logger.info(f"Downloaded APK for project {project_id}")
    return send_file(
        apk_path,
        as_attachment=True,
        download_name=f"{safe_filename}.apk",
        mimetype='application/vnd.android.package-archive'
    )
