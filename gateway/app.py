from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    tools = [
        {"name": "Password Generator", "url": "http://localhost:5007"},
        {"name": "Evil URL Shortener", "url": "http://localhost:5001"},
        {"name": "Password Strength Meter", "url": "http://localhost:5002"},
        {"name": "Hacker Clicker Game", "url": "http://localhost:5003"},
        {"name": "Security Buzzword Bingo", "url": "http://localhost:5004"},
        {"name": "Fake Breach Visualizer", "url": "http://localhost:5005"},
        {"name": "Phishing Email Generator", "url": "http://localhost:5006"},
    ]
    return render_template("index.html", tools=tools)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
