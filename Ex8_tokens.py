import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

#Create job and set variables
response1 = requests.get(url)
token = response1.json()["token"]
seconds = response1.json()["seconds"]

#Request before creating job
response2 = requests.get(url, params={"token": token})
assert response2.json()["status"] == "Job is NOT ready"
assert "result" not in response2.json()

#Waiting for creating job
time.sleep(seconds)

#Request after creating job
response3 = requests.get(url, params={"token": token})
assert response3.json()["status"] == "Job is ready"
assert "result" in response3.json()

