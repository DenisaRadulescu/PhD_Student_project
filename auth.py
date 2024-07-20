import json


"""Add user function"""


def add_user(path: str = "auth.json") -> bool:
    try:
        with open(path, "r") as f:
            credentials = json.loads(f.read())
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}.")
        return False
    else:
        username = input("Enter the new username: ")

        if username in credentials:
            print("Username already exists. Please choose a different username.")
            return False

        password = input("Enter the new password: ")
        confirm_new_password = input("Confirm the new password: ")
        while password != confirm_new_password:
            print("Passwords do not match. Please try again.")
            password = input("Enter the new password: ")
            confirm_new_password = input("Confirm the new password: ")

        credentials[username] = password

        try:
            with open(path, "w") as f:
                json.dump(credentials, f, indent=4)
        except IOError:
            print(f"Error writing to {path}.")
            return False

        print(f"User '{username}' added successfully.")
        return True




"""Create login function"""


def login(path: str = "auth.json", max_attempts: int = 3) -> str:
    with open(path, "r") as f:
        credentials = json.loads(f.read())

    # Username check with attempts
    attempts = 0
    username = input("Insert the user: ")

    while username not in credentials:
        attempts += 1
        if attempts >= max_attempts:
            print("Too many failed attempts. Exiting.")
            return None
        username = input("Wrong username. Please try again: ")

    # Password check with attempts
    attempts = 0
    password = input("Insert the password: ")

    while password != credentials[username]:
        attempts += 1
        if attempts >= max_attempts:
            print("Too many failed attempts. Exiting.")
            return None
        password = input("Wrong password. Please try again: ")

    print("Login successful.")
    return username

if __name__ == '__main__':
    # user = login()
    # if user:
    #     print(f"Welcome, {user}!")
    # else:
    #     print("Login failed.")

    new_user = add_user(path="auth.json")