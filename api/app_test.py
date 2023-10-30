from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == "Dinosaurs ruled the Earth 200 million years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_get_player_name():
    assert process_query("What is your name?") == "VWo50"


def test_plus():
    assert process_query("What is 50 plus 25?") == "75"


def test_mul():
    assert process_query("What is 20 multiplied by 21?") == "420"


def test_minus():
    assert process_query("What is 85 minus 91?") == "-6"


def test_square_cube():
    assert process_query("Which of the following numbers is both a square and a cube: 64, 1, 729?") == "64, 1, 729"


def test_are_primes():
    assert process_query("Which of the following numbers are primes: 88, 36, 11, 82, 7?") == "11, 7"
