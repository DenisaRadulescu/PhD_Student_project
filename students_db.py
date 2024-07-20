import json
import psycopg2 as ps
import connect_to_db as db



"""Fetch all students from the specified table"""


def select_all_students(config: dict, table: str = "phd_students.students") -> list:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"SELECT * FROM {table}"
                cursor.execute(sql_query)
                students = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                students_list = []
                for item in students:
                    students_list.append(dict(zip(columns, item)))

        return students_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


""" Print all students """


def show_all_students(students_list: list):
    for item in students_list:
        print(f"{item.get('student_id')}. {item.get('name')}")


"""Check if student id already exists or not"""


def student_id_exists(config: dict, student_id: int) -> bool:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM phd_students.students WHERE student_id = %s", (student_id,))
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"Eroare la verificarea ID-ului studentului: {e}")
        return False


""" Add a new student """


def add_student_to_db(config: dict, name: str, funding_type: str, scholarship: str, university_id: int,
                      table: str = "phd_students.students", ) -> bool:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"INSERT INTO {table} (name, funding_type, scholarship, university_id) VALUES (%s, %s, %s, %s);"
                cursor.execute(sql_query, (name, funding_type, scholarship, university_id))
                conn.commit()

        return True
    except Exception as e:
        print(f"Error on inserting into the database: {e}")
        return None


""" Select all published articles of all students"""


def select_articles_from_db(config: dict, table: str = "phd_students.articles") -> list:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"SELECT * FROM {table}"
                cursor.execute(sql_query)
                articles = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                articles_list = []
                for article in articles:
                    articles_list.append(dict(zip(columns, article)))

        return articles_list
    except Exception as e:
        print(f"Error on reading the database: {e}")
        return []


""" Show all articles within the list"""


def print_articles(articles: list):
    if not articles:
        print("No articles found.")
        return

    for index, article in enumerate(articles):
        print(f"Article {index + 1}:")
        for key, value in article.items():
            print(f"  {key}: {value}")
        print()

""" Add new articles within databse """


def add_article_to_db(config: dict, article_title: str, database: str, impact_factor: float,
                      student_id: int, student_first_author: str, coordinator_id: int,
                      coordinator_first_author: str, coordinator_co_author: str,
                      is_leader_coordinator: str, is_team_coordinator: str,
                      table: str = "phd_students.articles") -> bool:
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = f"""
                    INSERT INTO {table} (
                        article_title, database, impact_factor, student_id, student_first_author,
                        coordinator_id, coordinator_first_author, coordinator_co_author,
                        is_leader_coordinator, is_team_coordinator
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql_query, (
                    article_title, database, impact_factor, student_id, student_first_author,
                    coordinator_id, coordinator_first_author, coordinator_co_author,
                    is_leader_coordinator, is_team_coordinator))
                conn.commit()
        print("Article added successfully to the database!")
        return True
    except Exception as e:
        print(f"Error on inserting into the database: {e}")
        return False

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
    id = student_id_exists(config,2)
    print(id)

