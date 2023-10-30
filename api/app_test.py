from app import process_query


def test_knows_about_dinosaurs():
    str1 = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == str1


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_get_player_name():
    assert process_query("What is your name?") == "VWo50"


def maximum():
    assert process_query("Which of the following numbers is the \
    largest: 83, 43, 38?") == "83"


def maximum1():
    assert process_query("Which of the following numbers \
    is the largest: 21, 52, 23?") == "52"


def maximum2():
    assert process_query("Which of the following numbers \
    is the largest: 70, 9, 78?") == "78"
