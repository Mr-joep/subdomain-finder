from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
import subprocess

app = Flask(__name__)
script_process = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    text = data['text']
    number = data['number']
    with open('request/request-1.csv', 'a') as file:
        file.write(f"{text},{number}\n")
    return jsonify({"message": "Data saved successfully"})

@app.route('/load-data', methods=['GET'])
def load_data():
    file_names = {
        "in_progres_start": os.listdir('in-progres-start'),
        "in_progres": os.listdir('in-progres')
    }
    return jsonify(file_names)

@app.route('/load-results', methods=['GET'])
def load_results():
    results = {}
    for root, dirs, files in os.walk('results'):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            results[dir_name] = os.listdir(dir_path)
    return jsonify(results)

@app.route('/csv-viewer/<path:filename>')
def csv_viewer(filename):
    file_path = os.path.join('results', filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    try:
        df = pd.read_csv(file_path)
        table_html = df.to_html(classes='data', header="true").strip()
        return render_template('csv_viewer.html', table_html=table_html)
    except Exception as e:
        return str(e), 500

@app.route('/start-script', methods=['POST'])
def start_script():
    global script_process
    if script_process is None or script_process.poll() is not None:
        script_process = subprocess.Popen(['python3', 'controller-v1.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return jsonify({"message": "Script started"})
    else:
        return jsonify({"message": "Script is already running"})

@app.route('/stop-script', methods=['POST'])
def stop_script():
    global script_process
    if script_process is not None:
        script_process.terminate()
        script_process.wait()
        script_process = None
        return jsonify({"message": "Script stopped"})
    return jsonify({"message": "No script is running"})

if __name__ == '__main__':
    app.run(debug=True)
