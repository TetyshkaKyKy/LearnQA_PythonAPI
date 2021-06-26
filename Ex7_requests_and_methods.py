import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

print("--- case 1 ---")
response = requests.get(url)
print(f"Response for paramsless method request: {response.text}" + "\n") #'Wrong method provided'

print("--- case 2 ---")
response = requests.head(url, data={"method": "HEAD"})
print(f"Response for unsupported method: {response.text}" + "\n") #Nothing

print("--- case 3 ---")
response = requests.get(url, params={"method": "GET"})
print(f"Response for correct params method: {response.text}" + "\n") #{"success":"!"}


print("--- case 4 ---")
methods = ["GET", "POST", "PUT", "DELETE"]

for http_method in methods:
    print("\n" + f"Check {http_method} type")
    for params_method in methods:
        if http_method == "GET":
            response = requests.request(http_method, url, params={"method": params_method})
            print(f"Value for params method: {params_method}, response: {response.text}")
        else:
            response = requests.request(http_method, url, data={"method": params_method})
            print(f"Value for params method: {params_method}, response: {response.text}")