import json

"""Connet to database"""


def read_config(path: str = "config.json") -> dict:
    try:
        config = {}
        with open(path, "r") as f:
            config = json.loads(f.read())
        return config
    except Exception as e:
        print(f"Eroare la citire config. {e}")
        return config


if __name__ == '__main__':
    config = read_config()
    isi = read_isi_databases("isi_db.json")
    print(isi)
