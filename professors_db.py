import json

import psycopg2 as ps
import connect_to_db as db

# Read Config


# Fetch all professor from the specified table
def select_professors_from_db(config: dict, table: str = "phd_students.professors") -> list:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"SELECT * FROM {table}"
                cursor.execute(sql_query)
                professors= cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                professors_list = []
                for item in professors:
                    professors_list.append(dict(zip(columns, item)))

            return professors_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


# Show all professors
def show_all_professors(professors_list: list):
    # Print all universities
    for item in professors_list:
        print(f"{item.get('professor_id')}. {item.get('title')} {item.get('name')}")


# Add a new professor
def add_professor_to_db(config: dict, title: str, name: str, university_id: int, table: str = "phd_students.professors") -> bool:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"INSERT INTO {table} (title, name, university_id) VALUES (%s, %s, %s);"
                cursor.execute(sql_query, (title, name, university_id))
                conn.commit()

        return True
    except Exception as e:
        print(f"Error on adding a professor into the database: {e}")
        return None



if __name__ == '__main__':
    config = db.read_config()
    # proffs = select_universities_from_db(config)
    # print(proffs)
    # new_professor_id = add_professor_to_db(config, title="Dr.", name="Alice Johnson",
    #                                        university_id=3)
    # print("New Professor ID:", new_professor_id)
    professors = select_professors_from_db(config)
    show_all_professors(professors)
