import json

import psycopg2 as ps
import connect_to_db as db


def select_universities_from_db(config: dict, table: str = "phd_students.universities") -> list:
    """ Fetch all universities from the specified table """
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"SELECT * FROM {table}"
                cursor.execute(sql_query)
                universities = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                universities_list = []
                for item in universities:
                    universities_list.append(dict(zip(columns, item)))

            return universities_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


def show_all_universities(universities_list: list):
    """ Show all universities """
    # Print all universities
    for item in universities_list:
        print(f"{item.get('university_id')}. {item.get('faculty_name')}")


def add_university_to_db(config: dict, faculty_name: str, table: str = "phd_students.universities") -> bool:
    """ Add new university """
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"INSERT INTO {table} (faculty_name) VALUES (%s);"
                cursor.execute(sql_query, (faculty_name,))
                conn.commit()

        return True
    except Exception as e:
        print(f"Error on inserting into the database: {e}")
        return False


if __name__ == '__main__':
    config = db.read_config()
    # universities = select_universities_from_db(config)
    # show_all_universities(universities)
    new_university_id = add_university_to_db(config, faculty_name="Faculty of Computer Science")
    print("New University ID:", new_university_id)