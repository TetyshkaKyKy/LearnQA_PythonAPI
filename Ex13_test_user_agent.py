import requests
import pytest

platforms = [
    ({"user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
      "platform": "Mobile",
      "browser": "No",
      "device": "Android"}),
    ({"user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
      "platform": "Mobile",
      "browser": "Chrome",
      "device": "iOS"}),
    ({"user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
      "platform": "Googlebot",
      "browser": "Unknown",
      "device": "Unknown"}),
    ({"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
      "platform": "Web",
      "browser": "Chrome",
      "device": "No"}),
    ({"user_agent":"Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
      "platform": "Mobile",
      "browser": "No",
      "device": "iPhone"})
    ]

@pytest.mark.parametrize("user_agent", platforms)
def test_user_agent(user_agent):
    response = requests.get(
    "https://playground.learnqa.ru/ajax/api/user_agent_check",
    headers={"User-Agent": user_agent['user_agent']}
    )
    expected_platform = user_agent['platform']
    expected_browser = user_agent['browser']
    expected_device = user_agent['device']

    actual_platform = response.json()['platform']
    actual_browser = response.json()['browser']
    actual_device = response.json()['device']

    assert expected_platform == actual_platform, f"Platform {actual_platform} is incorrect. Expected platform is {expected_platform}."
    assert expected_browser == actual_browser, f"Browser {actual_browser} is incorrect. Expected browser is {expected_browser}."
    assert expected_device == actual_device, f"Device {actual_device} is incorrect. Expected device is {expected_device}."
