from flask import Flask, render_template, request, redirect, url_for, g
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/sdcard/insta'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'jpg', 'jpeg', 'png', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE'] = 'uploads.db'
app.config['SECRET_KEY'] = 'your_secret_key'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(app.config['DATABASE'])
    return g._database


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, '_database'):
        g._database.close()


@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM uploads')
    uploads = cur.fetchall()
    return render_template('index.html', uploads=uploads)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files')

    for file in files:
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            db = get_db()
            db.execute('INSERT INTO uploads (filename, path) VALUES (?, ?)',
                       [filename, file_path])
            db.commit()

    return 'Files uploaded successfully!'


if __name__ == '__main__':
    init_db()
    
    # Prompt user for the port number
    port = input("Enter the port number (e.g., 5000): ")
    
    # Run the app on the specified port
    app.run(debug=True, port=int(port))
