import psycopg2 as ps
import connect_to_db as db
import json



def get_isi_resources(file_path: str) -> list:
    """ Returns a JSON file containing ISI database
    information and returns a list of ISI resources"""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['isi_database']


def check_graduation_requirements(config: dict, student_id: int, isi_resources: list) -> dict:
    """ Check graduation requirements for a student """
    result = {
        "isi_articles": False,
        "cumulative_impact_factor": False,
        "student_first_author": False,
        "coordinator_co_author": False
    }

    try:
        # Connect to the database using the provided configuration
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Query to get all articles of the selected student
                sql_query = """
                SELECT * FROM phd_students.articles
                WHERE student_id = %s AND database = ANY(%s)
                """
                cursor.execute(sql_query, (student_id, isi_resources))
                articles = cursor.fetchall()

                # Initialize counters and flags
                isi_articles = 0
                cumulative_impact_factor = 0
                student_first_author = False
                coordinator_co_author = False

                # Check each article against the requirements
                for article in articles:
                    if article[2] in isi_resources:
                        isi_articles += 1
                        cumulative_impact_factor += article[3]
                        if article[5] == 'yes':
                            student_first_author = True
                        if article[8] == 'yes':
                            coordinator_co_author = True

                # Update result based on requirements
                result["isi_articles"] = isi_articles >= 2
                result["cumulative_impact_factor"] = cumulative_impact_factor >= 1.5
                result["student_first_author"] = student_first_author
                result["coordinator_co_author"] = coordinator_co_author

    except Exception as e:
        print(f"Error checking graduation requirements: {e}")

    return result


def print_graduation_status(student_id: int, requirements: dict):
    """Show graduation status for a student. Takes the results from
    check_graduation_requirements and prints a status
     that includes which requirements are not met if any """
    print(f"Student with ID {student_id}:")
    if all(requirements.values()):
        print("Has met all graduation requirements.")
    else:
        print("Has not met all graduation requirements. The following are still needed:")
        if not requirements["isi_articles"]:
            print("- Needs at least 2 ISI articles.")
        if not requirements["cumulative_impact_factor"]:
            print("- Needs a cumulative impact factor of at least 1.5.")
        if not requirements["student_first_author"]:
            print("- Needs to be first author on at least one article.")
        if not requirements["coordinator_co_author"]:
            print("- The coordinator needs to be co-author on at least one article.")

# def get_student_id(config: dict) -> int:
#     """Prompt user to enter a valid student ID"""
#     while True:
#         try:
#             student_id = int(input("Enter student ID: "))
#             if stud_db.student_id_exists(config, student_id):
#                 return student_id
#             else:
#                 print("The entered ID doesn't exist in the database. Please enter a valid ID.")
#         except ValueError:
#             print("Please enter a valid number.")


if __name__ == '__main__':
    config = db.read_config()
    isi_resources = get_isi_resources('isi_db.json')
    # # student_id = get_student_id(config)
    # requirements = check_graduation_requirements(config, student_id, isi_resources)
    # print_graduation_status(student_id, requirements)
