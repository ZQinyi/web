from app import process_query


def test_knows_about_dinosaurs():
    str1 = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == str1


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
