import json


def add_user(username: str, password: str, confirm_password: str, path: str = "auth.json") -> bool:
    """Add user function"""
    try:
        with open(path, "r") as f:
            credentials = json.loads(f.read())
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}.")
        return False

    if username in credentials:
        print("Username already exists. Please choose a different username.")
        return False

    if password != confirm_password:
        print("Passwords do not match.")
        return False

    credentials[username] = password

    try:
        with open(path, "w") as f:
            json.dump(credentials, f, indent=4)
    except IOError:
        print(f"Error writing to {path}.")
        return False

    print(f"User '{username}' added successfully.")
    return True


def login(username: str, password: str, path: str = "auth.json") -> str:
    """Create login function"""
    with open(path, "r") as f:
        credentials = json.loads(f.read())

    # Username check
    if username not in credentials:
        return None

    # Password check
    if password != credentials[username]:
        return None

    return username


if __name__ == '__main__':
    # user = login()
    # if user:
    #     print(f"Welcome, {user}!")
    # else:
    #     print("Login failed.")

    new_user = add_user(path="auth.json")