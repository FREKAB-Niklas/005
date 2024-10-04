from flask import Flask, request, jsonify, send_file
import yaml
import subprocess
import os

app = Flask(__name__)

# Set the output directory (using local directory for now)
output_dir = '/home/frekab005tester/005/backend/output'

@app.route('/process', methods=['POST'])
def process_wiring():
    data = request.json  # Get data from frontend
    
    # Convert data to Wireviz format (YAML)
    wireviz_data = {
        'cables': [{
            'id': 'Cable1',
            'wires': [
                {'id': 'Wire1', 'gauge': data['gauge'], 'from': data['source'], 'to': data['destination']}
            ]
        }]
    }

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file)
    
    # Run Wireviz to generate the diagram and output in the local directory
    subprocess.run(["wireviz", yaml_file_path])

    # Assume the generated PNG is now in the output directory
    png_file_path = os.path.join(output_dir, 'wireviz_data.png')

    # Read the YAML file content
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Return both YAML content and PNG file path
    return jsonify({
        "png_path": f"/{png_file_path}",  # The file path to serve the image
        "yaml_content": yaml_content      # The content of the YAML file
    })

# Serve static files (e.g., images) from the output directory
@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_file(os.path.join(output_dir, filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
