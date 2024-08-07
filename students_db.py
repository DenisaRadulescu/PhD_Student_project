import json
import psycopg2 as ps
import connect_to_db as db


def select_all_students(config: dict, table: str = "phd_students.students") -> list:
    """Fetch all students from the specified table"""
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # SQL query to join students and universities tables
                # This allows fetching university names instead of just IDs
                sql_query = f"""
                    SELECT s.*, u.faculty_name 
                    FROM {table} s
                    JOIN phd_students.universities u ON s.university_id = u.university_id
                """
                cursor.execute(sql_query)
                students = cursor.fetchall()
                # Get column names from cursor description
                columns = [desc[0] for desc in cursor.description]
                students_list = []
                # Create a list of dictionaries, each representing a student
                for item in students:
                    students_list.append(dict(zip(columns, item)))

        return students_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


def show_all_students(students_list: list) -> list:
    """ Print all students """
    for item in students_list:
        print(f"{item.get('student_id')}. {item.get('name')}")
    return students_list


def add_student_to_db(config: dict, name: str, funding_type: str, scholarship: str, university_id: int,
                      table: str = "phd_students.students") -> tuple:
    """ Add a new student if they do not already exist """
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check if the student already exists
                check_query = f"SELECT COUNT(*) FROM {table} WHERE name = %s AND university_id = %s;"
                cursor.execute(check_query, (name, university_id))
                count = cursor.fetchone()[0]

                if count > 0:
                    return False, f"Student {name} already exists at the given university."

                # If the student doesn't exist, add them
                sql_query = (f"INSERT INTO {table} (name, funding_type, scholarship, university_id)"
                             f" VALUES (%s, %s, %s, %s);")
                cursor.execute(sql_query, (name, funding_type, scholarship, university_id))
                conn.commit()

                return True, f"Student {name} added successfully."
    except Exception as e:
        print(f"Database Insert Error: {e}")
        return False, f"Error on inserting into the database: {e}"


def select_articles_from_db(config: dict, table: str = "phd_students.articles") -> list:
    """ Select all published articles of all students"""
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"SELECT * FROM {table}"
                cursor.execute(sql_query)
                articles = cursor.fetchall()
                # Get column names from cursor description
                columns = [desc[0] for desc in cursor.description]
                articles_list = []
                # Create a list of dictionaries, each representing an article
                for article in articles:
                    articles_list.append(dict(zip(columns, article)))

        return articles_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


def print_articles(articles: list):
    """ Show all articles within the list"""
    if not articles:
        print("No articles found.")
        return

    for index, article in enumerate(articles):
        print(f"Article {index + 1}:")
        for key, value in article.items():
            print(f"  {key}: {value}")
        print()


def validate_article_data(article_title: str, database: str, impact_factor: str,
                          student_id: str, coordinator_id: str) -> tuple:
    """
    Validates article data.
    Returns a tuple (is_valid, message).
    is_valid is True if all data is valid, False otherwise.
    message contains a success or error message.
    """
    if not article_title.strip():
        return False, "Article title cannot be empty."

    if not student_id.isnumeric():
        return False, "Invalid student ID. Use only integers."

    if not coordinator_id.isnumeric():
        return False, "Invalid coordinator ID. Use only integers."

    return True, "All input is valid."

def add_article_to_db(config: dict, article_title: str, database: str, impact_factor: str,
                      student_id: str, student_first_author: bool, coordinator_id: str,
                      coordinator_first_author: bool, coordinator_co_author: bool,
                      is_leader_coordinator: bool, is_team_coordinator: bool,
                      table: str = "phd_students.articles") -> tuple:
    """ Add a new article if it does not already exist"""

    # Validate input data
    is_valid, message = validate_article_data(
        article_title, database, impact_factor, student_id, coordinator_id
    )

    if not is_valid:
        return False, message

    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check if the article already exists
                check_query = f"SELECT COUNT(*) FROM {table} WHERE article_title = %s;"
                cursor.execute(check_query, (article_title,))
                if cursor.fetchone()[0] > 0:
                    return False, f"The article '{article_title}' already exists within the database."

                # If the article doesn't exist, add it
                sql_query = f"""
                    INSERT INTO {table} (
                        article_title, database, impact_factor, student_id, student_first_author,
                        coordinator_id, coordinator_first_author, coordinator_co_author,
                        is_leader_coordinator, is_team_coordinator
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql_query, (
                    article_title, database, float(impact_factor), int(student_id), student_first_author,
                    int(coordinator_id), coordinator_first_author, coordinator_co_author,
                    is_leader_coordinator, is_team_coordinator))
                conn.commit()
        return True, "Article added successfully to the database!"
    except Exception as e:
        return False, f"Error on inserting into the database: {e}"


if __name__ == '__main__':
    config = db.read_config()
    # students = select_all_students(config)
    # print(show_all_students(students))
    # new_student_id = add_student_to_db(config, name="Bob Brown", funding_type="buget", scholarship="yes", university_id=5)
    # print("New Student ID:", new_student_id)
    # pub_articles = select_articles_from_db(config)
    # # print(pub_articles)
    # print(print_articles(pub_articles))

    # new_article = add_article_to_db(config, article_title="testetested", database="IEEE Xplore",
    #                                 impact_factor=7.4, student_id=2, student_first_author="yes",
    #                                 coordinator_id=2, coordinator_first_author="yes",
    #                                 coordinator_co_author="yes", is_leader_coordinator="yes",
    #                                 is_team_coordinator="yes")
    # id = student_id_exists(config,2)
    # print(id)

