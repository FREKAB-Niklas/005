from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yaml
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the output directory where Wireviz outputs will be saved
output_dir = 'output'

@app.route('/process', methods=['POST'])
def process_wiring():
    data = request.json  # Get data from frontend

    # Extract pin counts from the request
    pincountX1 = int(data.get('pincountX1', 1))  # Default to 1 if not provided
    pincountX2 = int(data.get('pincountX2', 1))  # Default to 1 if not provided
    wirecolor = data.get('wirecolor', 'BK')  # Default to 'BK' (Black) if no color is selected

    # Now include connectors (with pincount) in wireviz_data
    wireviz_data = {
        'connectors': {
            'X1': {
                'type': 'Test1',
                'subtype': 'female',
                'pincount': pincountX1  # Include pin count for X1
            },
            'X2': {
                'type': 'Test2',
                'subtype': 'female',
                'pincount': pincountX2  # Include pin count for X2
            }
        }
    }

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')

    # First, dump connectors in block style
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file, sort_keys=False)

    # Now, manually write the cables section with flow-style for colors
    with open(yaml_file_path, 'a') as file:
        file.write('cables:\n')
        file.write(f'  B1:\n')
        file.write(f'    gauge: {data["gauge"]} AWG\n')
        file.write(f'    length: 0.2\n')
        file.write(f'    show_equiv: true\n')
        file.write(f'    colors: [{wirecolor}]\n')  # Flow-style color

    # Manually write the connections part with correct YAML formatting
    with open(yaml_file_path, 'a') as file:
        file.write('connections:\n')
        for connection in data['connections']:
            file.write('  -\n')
            for conn in connection:
                for key, value in conn.items():
                    file.write(f'    - {key}: {value}\n')

    # Run Wireviz to generate the diagram and output in the local directory
    subprocess.run(["wireviz", yaml_file_path])

    # Assume the generated PNG is now in the output directory
    png_file_path = os.path.join(output_dir, 'wireviz_data.png')

    # Read the YAML file content to display it
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_content = yaml_file.read()

    # Return both the PNG file path and the YAML content
    return jsonify({
        "png_path": f"/output/{os.path.basename(png_file_path)}",
        "yaml_content": yaml_content
    })

# Serve static files (e.g., images) from the output directory
@app.route('/output/<path:filename>')
def serve_output(filename):
    # Serve files from the output directory
    return send_file(os.path.join(output_dir, filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
