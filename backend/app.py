from flask import Flask, request, jsonify, send_file
import yaml
import subprocess
import os

app = Flask(__name__)

# Set the output directory where Wireviz outputs will be saved
output_dir = 'output'

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

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file)
    
    # Run Wireviz to generate the diagram and output in the local directory
    try:
        result = subprocess.run(["wireviz", yaml_file_path], capture_output=True, text=True)
        # Log the Wireviz output for debugging
        print("Wireviz stdout:", result.stdout)
        print("Wireviz stderr:", result.stderr)
        
        # Check if Wireviz returned an error
        if result.returncode != 0:
            return jsonify({"status": "error", "message": f"Wireviz failed: {result.stderr}"}), 500
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    # Assume the generated PNG is in the output directory
    png_file_path = os.path.join(output_dir, 'wireviz_data.png')

    # Read the YAML file content to display it
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Return both the PNG file path and the YAML content
    return jsonify({
        "png_path": f"/output/{os.path.basename(png_file_path)}",  # The relative path to the PNG
        "yaml_content": yaml_content                                # The YAML content to display
    })

# Serve static files (e.g., images) from the output directory
@app.route('/output/<path:filename>')
def serve_output(filename):
    # Serve files from the output directory
    return send_file(os.path.join(output_dir, filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
