complaint_api.py

from flask import Flask, request, jsonify import csv, os

app = Flask(name) COMPLAINT_FILE = 'complaints.csv'

@app.route('/api/complaints', methods=['POST']) def receive_complaint(): data = request.json required = ['name', 'email', 'subject', 'message'] if not all(field in data and data[field].strip() for field in required): return jsonify({'error': 'Missing fields'}), 400

file_exists = os.path.exists(COMPLAINT_FILE)
with open(COMPLAINT_FILE, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(required)
    writer.writerow([data['name'], data['email'], data['subject'], data['message']])

return jsonify({'message': 'Complaint submitted successfully'}), 200

if name == 'main': app.run(host='0.0.0.0', port=5000, debug=True)

