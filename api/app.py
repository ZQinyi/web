from flask import Flask, render_template, request
import re
import requests
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit_info", methods=["POST"])
def submit_info():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_major = request.form.get("major")
    return render_template("hello.html", name=input_name, age=input_age,
                           major=input_major)


@app.route("/submit_github", methods=["POST"])
def submit_github():
    input_name = request.form.get("GitHub_username")
    # Make sure to use requests.get here
    response = requests.get(f"https://api.github.com/users/{input_name}/repos")
    repos = []

    if response.status_code == 200:
        repos = response.json()  # data returned is a list of ‘repository’ entities
        # The following print will only display in the server's console (for debug purposes)
        for repo in repos:
            print(repo["full_name"])
    else:
        print(f"Error fetching repositories: {response.status_code}")

    # Pass both the username and the repos to the template
    return render_template("user.html", GitHub_username=input_name, repos=repos)


@app.route("/info", methods=["GET"])
def info():
    return render_template("info.html")


def process_query(q):
    add_match = re.search(r"What is (\d+) plus (\d+)?", q, re.I)
    add_mul = re.search(r"What is (\d+) multiplied by (\d+)?", q, re.I)
    add_minus = re.search(r"What is (\d+) minus (\d+)?", q, re.I)
    square_and_cube = re.search(r"Which of the following numbers is both a square and a cube: ([\d, ]+)?", q, re.I)
    are_primes = re.search(r"Which of the following numbers are primes: ([\d, ]+)?", q, re.I)
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif q == "asteroids":
        return "Unknown"
    elif q == "What is your name?":
        return "VWo50"
    elif add_match:
        num1, num2 = map(int, add_match.groups())
        return str(num1 + num2)
    elif add_mul:
        num1, num2 = map(int, add_mul.groups())
        return str(num1 * num2)
    elif add_minus:
        num1, num2 = map(int, add_minus.groups())
        return str(num1 - num2)
    elif square_and_cube:
        numbers_str = square_and_cube.groups()[0]
        numbers = [int(x) for x in numbers_str.split(", ")]
        result_numbers = [num for num in numbers if is_square_and_cube(num)]
        return ', '.join(map(str, result_numbers))
    elif are_primes:
        numbers_str = are_primes.groups()[0]
        numbers = [int(x) for x in numbers_str.split(", ")]
        primes = [str(num) for num in numbers if is_prime(num)]
        return ', '.join(primes)
    else:
        return "Unrecognized input!!!"


@app.route('/query', methods=['GET'])
def query_route():
    query = request.args.get('q')
    result = process_query(query)
    return result


def is_square_and_cube(n):
    root = round(n**(1/6))
    return root**6 == n


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
