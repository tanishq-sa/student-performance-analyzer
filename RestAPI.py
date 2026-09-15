import requests

url = 'https://jsonplaceholder.typicode.com/users'

response = requests.get(url)
if response.status_code == 200:
    users = response.json()
    print("Total Users: ", len(users))
    for user in users:
        print(user)
else:
    print("Error Code: ", response.status_code)




