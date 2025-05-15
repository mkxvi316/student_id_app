import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        password = request.form['password']
        photo = request.files['photo']

        if len(student_id) == 8 and student_id.isdigit():
            # 사진 저장
            if photo and photo.filename:
                filename = secure_filename(f"{student_id}.jpg")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(filepath)
                session['photo'] = f"uploads/{filename}"
            else:
                session['photo'] = 'default.jpg'  # 기본 사진

            session['name'] = name
            session['student_id'] = student_id
            session['expires_at'] = (datetime.utcnow() + timedelta(minutes=3)).isoformat() + 'Z'
            return redirect(url_for('id_card'))
        else:
            return "학번은 8자리 숫자여야 합니다."

    return render_template('login.html')

@app.route('/id')
def id_card():
    if 'name' not in session:
        return redirect(url_for('login'))

    return render_template('id_card.html',
                           name=session['name'],
                           student_id=session['student_id'],
                           expires_at=session['expires_at'],
                           photo=session.get('photo', 'default.jpg'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
