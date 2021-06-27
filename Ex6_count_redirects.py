import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
len_redirects = len(response.history)
past_url = response.url

print(f'Количество редиректов до итоговой точки: {len_redirects}')
print(f'Итоговый URL: {past_url}')