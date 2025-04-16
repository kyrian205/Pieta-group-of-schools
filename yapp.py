app.py

from flask import Flask, request, jsonify, send_from_directory import os, csv from werkzeug.utils import secure_filename from flask_cors import CORS

app = Flask(name) CORS(app)

--- Configs ---

UPLOAD_RESULT = 'uploaded_results' UPLOAD_PHOTOS = 'student_photos' GALLERY_FOLDER = 'gallery_images' STUDENT_FILE = 'students.csv' COMPLAINT_FILE = 'complaints.csv' NEWS_FILE = 'news.csv'

os.makedirs(UPLOAD_RESULT, exist_ok=True) os.makedirs(UPLOAD_PHOTOS, exist_ok=True) os.makedirs(GALLERY_FOLDER, exist_ok=True)

--- Student Registration ---

@app.route('/api/students/register', methods=['POST']) def register_student(): form = request.form photo = request.files.get('photo') if not photo or not all(k in form for k in ['username', 'password', 'fullname', 'gender', 'dob', 'class', 'math', 'english', 'science', 'comment']): return jsonify({'error': 'Missing fields'}), 400

filename = secure_filename(form['username'] + '.jpg')
photo.save(os.path.join(UPLOAD_PHOTOS, filename))

record = [
    form['username'], form['password'], form['fullname'], form['gender'], form['dob'], form['class'],
    form['math'], form['english'], form['science'], form.get('skills', ''), form['comment'], filename
]
write_csv(STUDENT_FILE, record, ["username", "password", "fullname", "gender", "dob", "class", "math", "english", "science", "skills", "comment", "photo"])
return jsonify({'message': 'Student registered'}), 200

@app.route('/api/students/list') def list_students(): return read_csv(STUDENT_FILE)

@app.route('/api/students/delete/<username>', methods=['DELETE']) def delete_student(username): return delete_row(STUDENT_FILE, username, key_index=0)

--- Result Uploads ---

@app.route('/api/results/upload', methods=['POST']) def upload_results(): if 'result_file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400 file = request.files['result_file'] filename = secure_filename(file.filename) path = os.path.join(UPLOAD_RESULT, filename) file.save(path) return jsonify({'message': 'Result uploaded'}), 200

--- Serve photos ---

@app.route('/student_photos/<filename>') def serve_photo(filename): return send_from_directory(UPLOAD_PHOTOS, filename)

--- Gallery Uploads ---

@app.route('/api/gallery/upload', methods=['POST']) def gallery_upload(): files = request.files.getlist('images') for f in files: f.save(os.path.join(GALLERY_FOLDER, secure_filename(f.filename))) return jsonify({'message': 'Uploaded'}), 200

@app.route('/gallery_images/<filename>') def gallery_image(filename): return send_from_directory(GALLERY_FOLDER, filename)

--- Complaints ---

@app.route('/api/complaints', methods=['POST']) def post_complaint(): data = request.json required = ['name', 'email', 'subject', 'message'] if not all(k in data and data[k].strip() for k in required): return jsonify({'error': 'Missing fields'}), 400 write_csv(COMPLAINT_FILE, [data[k] for k in required], required) return jsonify({'message': 'Complaint received'}), 200

@app.route('/api/complaints/list') def list_complaints(): return read_csv(COMPLAINT_FILE)

--- News Posting ---

@app.route('/api/news/post', methods=['POST']) def post_news(): data = request.json if not all(k in data for k in ['title', 'date', 'body']): return jsonify({'error': 'Missing fields'}), 400 write_csv(NEWS_FILE, [data[k] for k in ['title', 'date', 'body']], ['title', 'date', 'body']) return jsonify({'message': 'News saved'}), 200

@app.route('/api/news/list') def list_news(): return read_csv(NEWS_FILE)

--- Utilities ---

def write_csv(path, row, header): exists = os.path.exists(path) with open(path, 'a', newline='', encoding='utf-8') as f: w = csv.writer(f) if not exists: w.writerow(header) w.writerow(row)

def read_csv(path): if not os.path.exists(path): return jsonify([]) with open(path, newline='', encoding='utf-8') as f: return jsonify(list(csv.DictReader(f)))

def delete_row(path, value, key_index): if not os.path.exists(path): return jsonify({'error': 'File not found'}), 404 rows = [] deleted = False with open(path, newline='', encoding='utf-8') as f: reader = csv.reader(f) header = next(reader) for row in reader: if row[key_index] != value: rows.append(row) else: deleted = True with open(path, 'w', newline='', encoding='utf-8') as f: writer = csv.writer(f) writer.writerow(header) writer.writerows(rows) return jsonify({'deleted': deleted}), 200

if name == 'main': app.run(host='0.0.0.0', port=5000, debug=True)

