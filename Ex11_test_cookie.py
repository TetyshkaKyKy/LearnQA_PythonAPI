import requests

def test_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    homework_cookie = dict(response.cookies)
    print(homework_cookie)
    assert "HomeWork" in homework_cookie, "There is no 'homework' cookie in the response"
    assert homework_cookie["HomeWork"] == "hw_value", "The cookie value is incorrect"