from flask import Flask, render_template, request
from datetime import datetime, timedelta
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


@app.route("/hub")
def get_hub():
    return render_template("hub.html")


@app.route('/hub/submit_github', methods=['POST'])
def submit_github():
    username = request.form.get('GitHub_username')
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)
    contribution_graph = {}  # Dictionary to hold commit counts per day
    repos_info = []

    if repos_response.status_code == 200:
        repos = repos_response.json()
        for repo in repos:
            # Get the default branch
            default_branch = repo['default_branch']
            # Get commits from the last year for the default branch
            year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            commits_url = f"{repo['url']}/commits?since={year_ago}&sha={default_branch}"
            commits_response = requests.get(commits_url)
            if commits_response.status_code == 200:
                commits = commits_response.json()
                # additional data
                stargazers_count = repo['stargazers_count']
                forks_count = repo['forks_count']
                open_issues_count = repo['open_issues_count']
                # end additional data
                for commit in commits:
                    commit_date = commit['commit']['author']['date'][:10]  # Get just the date part
                    contribution_graph[commit_date] = contribution_graph.get(commit_date, 0) + 1
                    if commit == commits[0]:
                        commit_data = {
                            'commit_hash': commit['sha'],
                            'commit_author': commit['commit']['author']['name'],
                            'commit_date': commit_date,
                            'commit_message': commit['commit']['message']
                        }
                        repos_info.append({
                            'name': repo['name'],
                            'updated_at': repo['updated_at'],
                            'latest_commit': commit_data,
                            'stargazers_count': stargazers_count,
                            'forks_count': forks_count,
                            'open_issues_count': open_issues_count
                        })
            else:
                repos_info.append({
                    'name': repo['name'],
                    'updated_at': repo['updated_at'],
                    'latest_commit': {}
                })

        # Sort the contribution graph by date
        sorted_contributions = dict(sorted(contribution_graph.items()))

    else:
        return f"Failed to fetch repositories for user {username}, status code: {repos_response.status_code}"

    # Render template with repository and contribution graph information
    return render_template('user.html', username=username, repos=repos_info, contributions=sorted_contributions)


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
