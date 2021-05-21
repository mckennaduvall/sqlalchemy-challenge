from flask import Flask


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/about")
def about():
    name = "sia" 
    location = "Orange county"
    return f" My name is {name} and my county is {location}"

@app.route("/contact")
def contact():
    email = "siavash.mortezavi@gmail.com"
    
    return f"my {email}"

if __name__ == "__main__":
    app.run(debug=True)