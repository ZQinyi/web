from flask import Flask, render_template, request
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
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif q == "asteroids":
        return "Unknown"
    elif q == "What is your name?":
        return "VWo50"
    elif q == "Which of the following numbers is the largest: 83, 43, 38?":
        return "83"
    elif q == "Which of the following numbers is the largest: 21, 52, 23?":
        return "52"
    elif q == "Which of the following numbers is the largest: 70, 9, 78?":
        return "78"
    else:
        return "Unrecognized input!!!"


@app.route('/query', methods=['GET'])
def query_route():
    query = request.args.get('q')
    result = process_query(query)
    return result
