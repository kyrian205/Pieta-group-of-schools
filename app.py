app.py

from flask import Flask, request, jsonify import csv import os

app = Flask(name) CSV_FILE = 'admissions.csv'

@app.route('/api/admissions', methods=['POST']) def receive_admission(): data = request.form or request.json required_fields = ['fullname', 'dob', 'class', 'email', 'phone', 'address']

if not all(field in data and data[field].strip() for field in required_fields):
    return jsonify({'error': 'All fields are required.'}), 400

entry = [
    data['fullname'],
    data['dob'],
    data['class'],
    data['email'],
    data['phone'],
    data['address']
]

file_exists = os.path.exists(CSV_FILE)
with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(required_fields)
    writer.writerow(entry)

return jsonify({'message': 'Admission recorded successfully.'}), 200

if name == 'main': app.run(debug=True)

