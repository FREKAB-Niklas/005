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
    
    # Extract pin labels and pin colors from the request
    pinlabels_raw = data.get('pinlabels', "")
    pincolors_raw = data.get('pincolors', "")
    
    # Split by commas only if not empty
    pinlabels = pinlabels_raw.split(',') if pinlabels_raw else None
    pincolors = pincolors_raw.split(',') if pincolors_raw else None

    # Debugging prints (you can remove these later)
    print(f"Pin Labels: {pinlabels}")
    print(f"Pin Colors: {pincolors}")
    
    # Now include connectors (with pinlabels and pincolors) in wireviz_data
    wireviz_data = {
        'connectors': {
            'X1': {
                'type': 'Test1',
                'subtype': 'female'
            },
            'X2': {
                'type': 'Test2',
                'subtype': 'female'
            }
        },
        'cables': {
            'B1': {
                'gauge': f"{data['gauge']} AWG",
                'length': 0.2,
                'show_equiv': True
            }
        }
    }

    # Add pinlabels and pincolors only if they are provided
    if pinlabels and pinlabels != [""]:  # Ensure pinlabels are not empty
        wireviz_data['connectors']['X1']['pinlabels'] = pinlabels
        wireviz_data['connectors']['X2']['pinlabels'] = pinlabels

    if pincolors and pincolors != [""]:  # Ensure pincolors are not empty
        wireviz_data['connectors']['X1']['pincolors'] = pincolors
        wireviz_data['connectors']['X2']['pincolors'] = pincolors

    # Debugging print to check structure of wireviz_data (you can remove this later)
    print(f"Wireviz Data: {wireviz_data}")

    # Create connections based on the provided data
    connections = []
    for conn in data['connections']:
        source_conn = conn['source'].split(".")[0]
        dest_conn = conn['destination'].split(".")[0]
        source_pin = int(conn['source'].split(".")[1])  # Convert pin numbers to integers
        dest_pin = int(conn['destination'].split(".")[1])  # Convert pin numbers to integers

        # Construct connection as flow-style list
        connection = [
            {source_conn: [source_pin]},
            {'B1': [source_pin]},
            {dest_conn: [dest_pin]}
        ]
        connections.append(connection)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')

    # First, dump connectors and cables in block style
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file, sort_keys=False)

    # Manually write the connections part with correct YAML formatting
    with open(yaml_file_path, 'a') as file:
        file.write('connections:\n')
        for connection in connections:
            file.write('  -\n')
            for conn in connection:
                # Extract key and value from the dictionary (e.g., {'X1': [1]})
                for key, value in conn.items():
                    # Wrap each connection in an extra list to match Wireviz format
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
