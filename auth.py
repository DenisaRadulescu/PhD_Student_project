import json


def is_valid_password(password: str) -> bool:
    """Check if the password meets the criteria."""
    if len(password) < 6:
        return False

    has_upper = any(c.isupper() for c in password)  # At least one uppercase letter
    has_digit = any(c.isdigit() for c in password)  # At least one digit
    has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)  # At least one special character

    return has_upper and has_digit and has_special


def add_user(username: str, password: str, confirm_password: str, path: str = "auth.json") -> bool:
    """Add user function"""
    try:
        # Attempt to read existing credentials from the file
        with open(path, "r") as f:
            credentials = json.loads(f.read())
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}.")
        return False

    # Check if the username already exists
    if username in credentials:
        print("Username already exists. Please choose a different username.")
        return False

    # Verify that the passwords match
    if password != confirm_password:
        print("Passwords do not match.")
        return False

    # Validate the password criteria
    if not is_valid_password(password):
        print("Password must be at least 6 characters long, contain at least one uppercase letter, one digit, and one special character.")
        return False

    # Add the new user to the credentials dictionary
    credentials[username] = password

    try:
        # Write the updated credentials back to the file
        with open(path, "w") as f:
            json.dump(credentials, f, indent=4)
    except IOError:
        print(f"Error writing to {path}.")
        return False

    print(f"User '{username}' added successfully.")
    return True


def login(username: str, password: str, path: str = "auth.json") -> str:
    """Create login function"""
    try:
        # Read credentials from the file
        with open(path, "r") as f:
            credentials = json.loads(f.read())
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {path}.")
        return None

    # Check if the username exists
    if username not in credentials:
        return None

    # Verify the password
    if password != credentials[username]:
        return None

    # Return the username if login is successful
    return username


if __name__ == '__main__':
    # user = login()
    # if user:
    #     print(f"Welcome, {user}!")
    # else:
    #     print("Login failed.")

    new_user = add_user(path="auth.json")