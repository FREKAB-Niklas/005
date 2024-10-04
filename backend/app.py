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

        # Construct connection using flow style for lists
        connection = [
            {source_conn: [source_pin]},  # Ensure this is a flow list
            {'B1': [source_pin]},  # Use list for the cable pin connection
            {dest_conn: [dest_pin]}  # Ensure this is also a flow list
        ]

        # Append the connection to the connections list
        connections.append(connection)

    wireviz_data = {
        'connectors': connectors,
        'cables': {
            'B1': {
                'gauge': f"{data['gauge']} AWG",  # Convert gauge from input
                'length': 0.2,  # Example length, modify as needed
                'show_equiv': True,  # Example of auto-calculated AWG equivalent from metric gauge
            }
        }
    }

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save YAML file in the output directory using default dump for connectors and cables
    yaml_file_path = os.path.join(output_dir, 'wireviz_data.yaml')

    # First, dump connectors and cables in block style
    with open(yaml_file_path, 'w') as file:
        yaml.dump(wireviz_data, file, sort_keys=False)

    # Now append connections in block style, ensuring each connection is dumped correctly
    with open(yaml_file_path, 'a') as file:
        file.write('connections:\n')
        for connection in connections:
            file.write('  - ')  # Start the connection in block format
            yaml.dump(connection, file, default_flow_style=True, sort_keys=False)

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
