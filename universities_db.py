import json

import psycopg2 as ps
import connect_to_db as db


def select_universities_from_db(config: dict, table: str = "phd_students.universities") -> list:
    """ Fetch all universities from the specified table """
    try:
        # Establish a connection to the database using the provided configuration
        with ps.connect(**config) as conn:
            # Open a cursor to perform database operations
            with conn.cursor() as cursor:
                # Define the SQL query to select all records from the specified table
                sql_query = f"SELECT * FROM {table}"
                # Execute the SQL query
                cursor.execute(sql_query)
                # Fetch all rows from the executed query
                universities = cursor.fetchall()
                # Get the column names from the cursor description
                columns = [desc[0] for desc in cursor.description]
                # Initialize an empty list to store the university records as dictionaries
                universities_list = []
                # Iterate over each fetched row
                for item in universities:
                    # Zip the column names with the row data to create a dictionary
                    universities_list.append(dict(zip(columns, item)))

            # Return the list of dictionaries, each representing a university
            return universities_list
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"Error on reading the database: {e}")
        # Return an empty list in case of an error
        return []


def show_all_universities(universities_list: list) -> list:
    """ Show all universities """
    # Print all universities
    for item in universities_list:
        print(f"{item.get('university_id')}. {item.get('faculty_name')}")
    return universities_list


def validate_university_data(faculty_name: str) -> tuple:
    """
    Validates university data.
    Returns a tuple (is_valid, message).
    is_valid is True if all data is valid, False otherwise.
    message contains a success or error message.
    """
    if not faculty_name.strip():
        return False, "Faculty name cannot be empty."

    if not all(char.isalpha() or char.isspace() for char in faculty_name):
        return False, "Invalid faculty name. Use only letters and spaces."

    return True, "All input is valid."


def add_university_to_db(config: dict, faculty_name: str, table: str = "phd_students.universities") -> tuple:
    """ Add new university if it doesn't already exist """
    # Validate the input data
    is_valid, message = validate_university_data(faculty_name)
    if not is_valid:
        return False, message

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # First, check if the university already exists
                check_query = f"SELECT COUNT(*) FROM {table} WHERE faculty_name = %s;"
                cursor.execute(check_query, (faculty_name,))
                count = cursor.fetchone()[0]

                if count > 0:
                    return False, f"University with faculty name '{faculty_name}' already exists."

                # If the university doesn't exist, add it
                insert_query = f"INSERT INTO {table} (faculty_name) VALUES (%s);"
                cursor.execute(insert_query, (faculty_name,))
                conn.commit()

                return True, f"University with faculty name '{faculty_name}' added successfully."
    except Exception as e:
        return False, f"Error on adding a university to the database: {e}"


if __name__ == '__main__':
    config = db.read_config()
    # universities = select_universities_from_db(config)
    # show_all_universities(universities)
    new_university_id = add_university_to_db(config, faculty_name="Faculty of Computer Science")
    print("New University ID:", new_university_id)