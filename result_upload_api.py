result_upload_api.py

from flask import Flask, request, jsonify import os import csv from werkzeug.utils import secure_filename

app = Flask(name) UPLOAD_FOLDER = 'uploaded_results' os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/results/upload', methods=['POST']) def upload_results(): if 'result_file' not in request.files: return jsonify({'error': 'No file part in request'}), 400

file = request.files['result_file']
if file.filename == '':
    return jsonify({'error': 'No file selected'}), 400

filename = secure_filename(file.filename)
filepath = os.path.join(UPLOAD_FOLDER, filename)
file.save(filepath)

# Optionally validate CSV content (headers, etc)
with open(filepath, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader, None)
    if header and 'username' not in [h.lower() for h in header]:
        return jsonify({'error': 'Invalid file format: username column required'}), 400

return jsonify({'message': 'Result file uploaded successfully'}), 200

if name == 'main': app.run(debug=True)

