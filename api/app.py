from flask import Flask, render_template, request
import re
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_major = request.form.get("major")
    return render_template("hello.html", name=input_name, age=input_age,
                           major=input_major)


@app.route("/info", methods=["GET"])
def info():
    return render_template("info.html")


def process_query(q):
    add_match = re.search(r"what is (\d+) plus (\d+)?", q, re.I)
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif q == "asteroids":
        return "Unknown"
    elif q == "What is your name?":
        return "VWo50"
    elif add_match:
        num1, num2 = map(int, add_match.groups())
        return str(num1 + num2)
    else:
        return "Unrecognized input!!!"


@app.route('/query', methods=['GET'])
def query_route():
    query = request.args.get('q')
    result = process_query(query)
    return result
