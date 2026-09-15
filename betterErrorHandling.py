import requests

url = "https://jsonplaceholder.typicode.com/users"
try:
    response = requests.get(url)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(user['email'], user['name'])
    else:
        print("Error Code: ", response.status_code)
except Exception as e:
    print(e)