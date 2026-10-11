from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>ABBA Website</title></head>
    <body style='text-align:center; font-family:Arial; padding-top:80px; background:#f0f0f0'>
        <h1>Assalamu Alaikum! 👋</h1>
        <h2 style='color:green'>Website na ABBA yana aiki! ✅</h2>
        <p>An kirkire shi daga KARKARKU</p>
        <button style='padding:10px 20px; background:black; color:white; border-radius:10px'>Welcome</button>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
