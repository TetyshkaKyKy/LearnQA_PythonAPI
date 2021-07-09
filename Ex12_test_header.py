import requests


def test_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    homework_headers = response.headers

    assert "x-secret-homework-header" in homework_headers, "There is no 'homework' header in the response"
    assert homework_headers["x-secret-homework-header"] == "Some secret value", "The header value is incorrect"