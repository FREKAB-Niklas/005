from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yaml
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the output directory where Wireviz outputs will be saved
output_dir = 'output'

# Custom YAML dumper to force flow style for lists in connections
class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow=flow, indentless=False)

    def represent_dict(self, data):
        if isinstance(data, dict):
            return self.represent_mapping('tag:yaml.org,2002:map', data)
        return super().represent_dict(data)

    def represent_list(self, data):
        # Force flow style (i.e., use [1, 2, 3]) for lists
        return self.represent_sequence('tag:yaml.org,2002:seq', data, flow=True)

yaml.add_representer(list, MyDumper.represent_list)

@app.route('/process', methods=['POST'])
def process_wiring():
    data = request.json  # Get data from frontend

    # Convert data to the simplified Wireviz format (YAML)
    connectors = {
        'X1': {
            'type': 'Test1',
            'subtype': 'female'
        },
        'X2': {
            'type': 'Test2',
            'subtype': 'female'
        }
    }

    # Create connections based on the provided data
    connections = []
    for conn in data['connections']:
        source_conn = conn['source'].split(".")[0]
        dest_conn = conn['destination'].split(".")[0]
        source_pin = int(conn['source'].split(".")[1])  # Convert pin numbers to integers
        dest_pin = int(conn['destination'].split(".")[1])  # Convert pin numbers to integers
        
        connections.append([
            {source_conn: [source_pin]},  # Use list ([]) instead of string
            {'B1': [source_pin]},  # Use list for cable pin connection
            {dest_conn: [dest_pin]}  # Use list for destination pin
        ])

    wireviz_data = {
        'connectors': connectors,
        'cables': {
            'B1': {
                'gauge': f"{data['gauge']} AWG",  # Convert gauge from input
                'length': 0.2,  # Example length, modify as needed
                'show_equiv': True,  # Example of auto-calculated AWG equivalent from metric gauge
            }
        },
        'connections': connections
    }

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory using the custom dumper
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file, Dumper=MyDumper, sort_keys=False)

    # Run Wireviz to generate the diagram and output in the local directory
    subprocess.run(["wireviz", yaml_file_path])

    # Assume the generated PNG is now in the output directory
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
