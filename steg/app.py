from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
from steg_logic import embed_message
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Very simple in-memory users (no DB for now)
users = {'admin': 'pass123'}

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users[request.form['username']] = request.form['password']
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if users.get(request.form['username']) == request.form['password']:
            session['user'] = request.form['username']
            return redirect(url_for('upload'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        carrier = request.files['carrier']
        message = request.files['message']
        start_bit = int(request.form['start_bit'])
        l = int(request.form['l'])

        carrier_path = os.path.join(UPLOAD_FOLDER, secure_filename(carrier.filename))
        output_path = os.path.join(UPLOAD_FOLDER, "stego_" + secure_filename(carrier.filename))

        carrier.save(carrier_path)
        message_path = os.path.join(UPLOAD_FOLDER, secure_filename(message.filename))
        message.save(message_path)

        embed_message(carrier_path, message_path, output_path, start_bit, l)
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
