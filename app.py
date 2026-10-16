from flask import Flask, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "abba_sirri_12345"

# Wurin adana users - zai tafi Render
users = {}

# Lesson 1000
lessons = []
for i in range(1, 1001):
    lessons.append({"id": i, "title": f"Lesson {i}", "content": f"Wannan shine darasi na {i}. Anan zaka koyi Cyber Security, Ethical Hacking da Programming."})

# HTML Guda Daya
HTML_BASE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ABBA - 1000 Lessons</title>
<style>
body{font-family:Arial;background:#0f172a;color:white;padding:20px}
.container{max-width:900px;margin:auto;background:#1e293b;padding:20px;border-radius:12px}
input{width:95%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #334155;background:#0f172a;color:white}
button{padding:12px 20px;background:#38bdf8;border:none;border-radius:8px;font-weight:bold;cursor:pointer}
.box{border:1px solid #334155;padding:15px;border-radius:10px;margin:10px 0;background:#0f172a}
.lesson{background:#0f172a;padding:10px;margin:5px;border-radius:6px;border:1px solid #334155}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
a{color:#38bdf8}
</style>
</head>
<body>
<div class="container">
%s
</div>
</body>
</html>
"""

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    content = """
    <h1 style='text-align:center'>Barka da zuwa ABBA Website</h1>
    <div style='display:flex;gap:10px;justify-content:center;flex-wrap:wrap'>
      <div class='box'><h2>Register</h2>
        <form action='/register' method='post'>
          <input name='username' placeholder='Username' required>
          <input name='email' placeholder='Email' required>
          <input name='password' type='password' placeholder='Password' required>
          <button>Register</button>
        </form>
      </div>
      <div class='box'><h2>Login</h2>
        <form action='/login' method='post'>
          <input name='email' placeholder='Email' required>
          <input name='password' type='password' placeholder='Password' required>
          <button>Login</button>
        </form>
      </div>
    </div>
    <p style='text-align:center;margin-top:20px'>Password ana adanawa a Render da hash!</p>
    """
    return HTML_BASE % content

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if email in users:
        return HTML_BASE % "<h2>Email ya riga yayi register!</h2><a href='/'>Koma</a>"
    users[email] = {"username": username, "password": generate_password_hash(password)}
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users.get(email)
    if not user or not check_password_hash(user['password'], password):
        return HTML_BASE % "<h2>Email ko Password ba daidai ba!</h2><a href='/'>Koma</a>"
    session['user'] = email
    session['username'] = user['username']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    username = session['username']
    lesson_html = ""
    for l in lessons[:50]: # Nuna 50 na farko don kar ya yi nauyi, sauran da search
        lesson_html += f"<div class='lesson'><b>{l['title']}</b><br><small>{l['content']}</small></div>"

    content = f"""
    <h2>Sannu {username}!</h2>
    <p>Kana da Lesson {len(lessons)} gaba daya!</p>
    <a href='/logout'><button style='background:#ef4444;color:white'>Logout</button></a>
    <a href='/lessons'><button> Duba Duk Lesson 1000</button></a>
    <h3 style='margin-top:20px'>Lessons 50 na farko:</h3>
    <div class='grid'>{lesson_html}</div>
    """
    return HTML_BASE % content

@app.route('/lessons')
def all_lessons():
    if 'user' not in session:
        return redirect('/')
    all_html = "".join([f"<div class='lesson'><b>{l['title']}</b><br><small>{l['content']}</small></div>" for l in lessons])
    content = f"<h2>Duk Lessons 1000</h2><a href='/dashboard'>Koma Dashboard</a><div class='grid' style='margin-top:15px'>{all_html}</div>"
    return HTML_BASE % content

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))