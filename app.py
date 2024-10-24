from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import yaml
import tempfile
import shutil
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
CORS(app)

# Create a temp directory for storing files
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/api/generate-diagram', methods=['POST'])
def generate_diagram():
    try:
        data = request.json
        yaml_content = data.get('yaml')
        
        if not yaml_content:
            return jsonify({'success': False, 'error': 'No YAML content provided'}), 400

        # Create unique filename using timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        yaml_path = os.path.join(TEMP_DIR, f'wireviz_{timestamp}.yml')
        
        # Write YAML content to file
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        # Run wireviz command
        exit_code = os.system(f'wireviz {yaml_path}')
        
        if exit_code != 0:
            return jsonify({'success': False, 'error': 'Failed to generate diagram'}), 500
        
        # Get the generated PNG file path
        png_path = yaml_path.replace('.yml', '.png')
        
        if not os.path.exists(png_path):
            return jsonify({'success': False, 'error': 'Diagram file not generated'}), 500
        
        # Return the relative path to the PNG file
        return jsonify({
            'success': True,
            'imageUrl': f'/temp/wireviz_{timestamp}.png'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def cleanup_old_files():
    """Remove files older than 1 hour from the temp directory"""
    while True:
        try:
            current_time = datetime.now()
            for filename in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if current_time - file_modified > timedelta(hours=1):
                    os.remove(file_path)
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(3600)  # Sleep for 1 hour

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

# Serve static files from temp directory
@app.route('/temp/<path:filename>')
def serve_file(filename):
    return send_file(os.path.join(TEMP_DIR, filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)