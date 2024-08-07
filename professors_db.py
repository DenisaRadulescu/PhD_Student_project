import json

import psycopg2 as ps
import connect_to_db as db


def select_professors_from_db(config: dict, table: str = "phd_students.professors") -> list:
    """ Fetch all professor from the specified table """
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"""
                SELECT p.professor_id, p.title, p.name, p.university_id, u.faculty_name 
                FROM {table} p
                JOIN phd_students.universities u ON p.university_id = u.university_id
                """
                cursor.execute(sql_query)
                professors = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                professors_list = []
                for item in professors:
                    professors_list.append(dict(zip(columns, item)))

            return professors_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


def show_all_professors(professors_list: list) -> list:
    """Show all professors as a list"""
    for item in professors_list:
        print(f"{item.get('professor_id')}. {item.get('title')} {item.get('name')} - {item.get('faculty_name')}")
    return professors_list


def validate_professor_data(title: str, name: str, university_id: str) -> tuple:
    """
    Validates professor data.
    Returns a tuple (is_valid, message).
    is_valid is True if all data is valid, False otherwise.
    message contains a success or error message.
    """
    # if not all(char.isalpha() or char.isspace() for char in title):
    #     return False, "Invalid title. Use only letters and spaces."
    #
    # if not all(char.isalpha() or char.isspace() for char in name):
    #     return False, "Invalid name. Use only letters and spaces."

    if not university_id.isnumeric():
        return False, "Invalid university ID. Use only numbers."

    return True, "All input is valid."


def add_professor_to_db(config: dict, title: str, name: str, university_id: int,
                        table: str = "phd_students.professors") -> tuple:
    """ Add a new professor if they don't already exist """
    # Validate the input data
    is_valid, message = validate_professor_data(title, name, str(university_id))
    if not is_valid:
        return False, message

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # First, check if the professor already exists
                check_query = f"SELECT COUNT(*) FROM {table} WHERE name = %s AND university_id = %s;"
                cursor.execute(check_query, (name, university_id))
                count = cursor.fetchone()[0]

                if count > 0:
                    return False, f"Professor {name} already exists at the given university."

                # If the professor doesn't exist, add them
                insert_query = f"INSERT INTO {table} (title, name, university_id) VALUES (%s, %s, %s);"
                cursor.execute(insert_query, (title, name, university_id))
                conn.commit()

                return True, f"Professor {name} added successfully."
    except Exception as e:
        return False, f"Error on adding a professor into the database: {e}"



if __name__ == '__main__':
    config = db.read_config()
    # proffs = select_universities_from_db(config)
    # print(proffs)
    # new_professor_id = add_professor_to_db(config, title="Dr.", name="Alice Johnson",
    #                                        university_id=3)
    # print("New Professor ID:", new_professor_id)
    professors = select_professors_from_db(config)
    show_all_professors(professors)
