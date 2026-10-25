import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    users = response.json()
    print("Total Users:", len(users))
    print()

    for user in users:
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Phone: {user['phone']}")
        print(f"City: {user['address']['city']}")
        print(f"Company: {user['company']['name']}")
        print("-" * 40)

    demo_city = "Gwenborough"
    print(f"\n--- Demo: Searching for city '{demo_city}' ---")
    demo_found = False
    for user in users:
        if user['address']['city'].lower() == demo_city.lower():
            print(f"  Name: {user['name']}")
            print(f"  Email: {user['email']}")
            demo_found = True
    if not demo_found:
        print(f"  No user found in '{demo_city}'.")

    print()
    search = input("Enter City Name to Search: ")
    found = False
    for user in users:
        if user['address']['city'].lower() == search.lower():
            print(f"Name: {user['name']}")
            print(f"Email: {user['email']}")
            found = True

    if not found:
        print("No user found in that city.")
else:
    print("Error Code:", response.status_code)
