import requests

userID = input("Enter User ID: ")
url = 'https://jsonplaceholder.typicode.com/users/' + userID
try:
    response = requests.get(url)
    if len(response.json()) > 0 or len(response.json()) > 10:
        if response.status_code == 200:
            data = response.json()
            print("\n--User Info--")
            print("Name: ", data['name'])
            print("Email: ", data['email'])
            print("Phone: ", data['phone'])
            print("City: ", data['address']['city'])
            print("Company: ", data['company']['name'])
        else:
            print("Error Code: ", response.status_code)
    else:
        print("User Not Found")
except Exception as e:
    print(e)
