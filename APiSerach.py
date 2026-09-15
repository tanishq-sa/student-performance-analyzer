import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
if response.status_code == 200:
    users = response.json()
    search = input("Enter City Name: ")
    for user in users:
        if user['address']['city'].lower() == search.lower():
            print("Name", user['name'])
            print("Email: ", user['email'])
else:
    print("Result not found")