admission_api.py

from flask import Flask, request, jsonify from flask_mail import Mail, Message

app = Flask(name)

Mail configuration (use real credentials in production)

app.config['MAIL_SERVER'] = 'smtp.gmail.com' app.config['MAIL_PORT'] = 587 app.config['MAIL_USE_TLS'] = True app.config['MAIL_USERNAME'] = 'admissions@pietaschools.edu' app.config['MAIL_PASSWORD'] = 'Donk123' app.config['MAIL_DEFAULT_SENDER'] = 'admissions@pietaschools.edu'

mail = Mail(app)

@app.route('/api/admissions', methods=['POST']) def handle_admission(): data = request.form fullname = data.get('fullname') email = data.get('email') if not fullname or not email: return jsonify({'error': 'Fullname and email are required'}), 400

try:
    msg = Message(
        subject="Pieta School Admission Confirmation",
        recipients=[email],
        body=f"Dear {fullname},\n\nThank you for applying to Pieta Group of Schools. We have received your application and will contact you shortly.\n\nRegards,\nPieta School Admin"
    )
    mail.send(msg)
    return jsonify({'message': 'Application received and email sent.'}), 200
except Exception as e:
    return jsonify({'error': str(e)}), 500

if name == 'main': app.run(debug=True)

