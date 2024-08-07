import json


def read_config(path: str = "config.json") -> dict:
    """Read configuration from a JSON file"""
    try:
        config = {}
        # Attempt to open and read the configuration file
        with open(path, "r") as f:
            config = json.loads(f.read())
        return config
    except Exception as e:
        # Handle any exceptions that occur during file reading or JSON parsing
        print(f"Error reading config: {e}")
        return config


if __name__ == '__main__':
    config = read_config()

