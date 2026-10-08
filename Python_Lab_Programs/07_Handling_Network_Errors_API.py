import requests


def fetch_user_data(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            print("User Not Found")
            return

        print("\n--User Info--")
        print("Name:", data['name'])
        print("Email:", data['email'])
        print("Phone:", data['phone'])
        print("City:", data['address']['city'])
        print("Company:", data['company']['name'])

    except requests.exceptions.ConnectionError:
        print("Network Error: Unable to connect to the server.")
        print("Please check your internet connection.")

    except requests.exceptions.Timeout:
        print("Timeout Error: The server took too long to respond.")
        print("Please try again later.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        if e.response.status_code == 404:
            print("User not found.")
        elif e.response.status_code == 500:
            print("Server error. Please try again later.")
        else:
            print(f"Unexpected HTTP error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")


def fetch_all_users():
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        users = response.json()
        print(f"\nTotal Users: {len(users)}\n")
        for user in users:
            print(f"{user['name']} - {user['email']}")

    except requests.exceptions.ConnectionError:
        print("Network Error: Unable to connect to the server.")

    except requests.exceptions.Timeout:
        print("Timeout Error: The server took too long to respond.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")


if __name__ == "__main__":

    print("=" * 50)
    print("  Handling Network Errors - Public API")
    print("=" * 50)

    print("\n--- Fetching All Users ---")
    fetch_all_users()

    print("\n--- Fetching Individual User ---")
    userID = input("Enter User ID (1-10): ")
    fetch_user_data(userID)

    print("\n--- Testing Invalid URL ---")
    try:
        response = requests.get("https://invalid-url-test.example.com", timeout=5)
    except requests.exceptions.ConnectionError:
        print("Caught ConnectionError: Cannot reach invalid-url-test.example.com")

    print("\n" + "=" * 50)
    print("  Demo Complete")
    print("=" * 50)
