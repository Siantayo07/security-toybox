from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length=12, uppercase=True, lowercase=True, numbers=True, symbols=True):
    chars = ""
    
    if uppercase:
        chars += string.ascii_uppercase
    if lowercase:
        chars += string.ascii_lowercase
    if numbers:
        chars += string.digits
    if symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character set is selected
    if not chars:
        chars = string.ascii_letters + string.digits
    
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        uppercase = 'uppercase' in request.form
        lowercase = 'lowercase' in request.form
        numbers = 'numbers' in request.form
        symbols = 'symbols' in request.form
        
        password = generate_password(length, uppercase, lowercase, numbers, symbols)
    
    return render_template("index.html", password=password)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
