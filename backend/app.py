from flask import Flask, request, jsonify
import yaml
import subprocess

app = Flask(__name__)

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
    with open('wireviz_data.yaml', 'w') as file:
        yaml.dump(wireviz_data, file)
    
    # Run Wireviz to generate diagram
    subprocess.run(["wireviz", "wireviz_data.yaml"])
    
    return jsonify({"status": "success", "message": "Diagram generated"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
