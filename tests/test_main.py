from package.main import greet


def test_greet():
    assert greet("Thomas") == "Hello Thomas!"
    assert greet(1234) == "Hello 1234!"
