news_api.py

from flask import Flask, request, jsonify import csv, os

app = Flask(name) NEWS_FILE = 'news.csv'

@app.route('/api/news/post', methods=['POST']) def post_news(): data = request.json if not all(k in data for k in ['title', 'date', 'body']): return jsonify({'error': 'Missing fields'}), 400

file_exists = os.path.exists(NEWS_FILE)
with open(NEWS_FILE, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(['title', 'date', 'body'])
    writer.writerow([data['title'], data['date'], data['body']])

return jsonify({'message': 'News posted'}), 200

@app.route('/api/news/list', methods=['GET']) def list_news(): if not os.path.exists(NEWS_FILE): return jsonify([]) with open(NEWS_FILE, newline='', encoding='utf-8') as f: reader = csv.DictReader(f) return jsonify(list(reader))

if name == 'main': app.run(debug=True)

