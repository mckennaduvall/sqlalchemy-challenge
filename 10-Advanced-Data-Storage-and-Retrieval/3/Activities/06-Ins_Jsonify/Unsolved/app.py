from flask import Flask, jsonify

app = Flask(__name__)

hello_dict = {"hello": "world!"}

countries = ['ireland', 'canada', 'chile', 'saudi arabia']



@app.route("/")
def home():
    return jsonify(countries)

@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)

@app.route("/taking_inputs/<my_name>")
def name(my_name):
    return my_name.upper()



if __name__ == "__main__":
    app.run(debug = True)