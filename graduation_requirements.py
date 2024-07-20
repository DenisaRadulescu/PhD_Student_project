import psycopg2 as ps
import connect_to_db as db
import json
import students_db as stud_db

"""Read ISI databse for further usage"""


def get_isi_resources(file_path: str) -> list:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['isi_database']


""" Make graduation requirements """


def check_graduation_requirements(config: dict, student_id: int, isi_resources: list) -> dict:
    result = {
        "isi_articles": False,
        "cumulative_impact_factor": False,
        "student_first_author": False,
        "coordinator_co_author": False
    }
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Check all the articles of the selected student by ID
                sql_query = """
                SELECT * FROM phd_students.articles
                WHERE student_id = %s AND database = ANY(%s)
                """
                cursor.execute(sql_query, (student_id, isi_resources))
                articles = cursor.fetchall()

                # Check requirements
                isi_articles = 0
                cumulative_impact_factor = 0
                student_first_author = False
                coordinator_co_author = False

                for article in articles:
                    if article[2] in isi_resources:
                        isi_articles += 1
                        cumulative_impact_factor += article[3]
                        if article[5] == 'yes':
                            student_first_author = True
                        if article[8] == 'yes':
                            coordinator_co_author = True

                # Check if requirements are met and update the result
                result["isi_articles"] = isi_articles >= 2
                result["cumulative_impact_factor"] = cumulative_impact_factor >= 1.5
                result["student_first_author"] = student_first_author
                result["coordinator_co_author"] = coordinator_co_author

    except Exception as e:
        print(f"Eroare la verificarea cerințelor de absolvire: {e}")

    return result


"""Show if the student passed or not"""


def print_graduation_status(student_id: int, requirements: dict):
    print(f"Studentul cu ID-ul {student_id}:")
    if all(requirements.values()):
        print("A îndeplinit toate cerințele de absolvire.")
    else:
        print("Nu a îndeplinit toate cerințele de absolvire. Trebuie să mai facă următoarele:")
        if not requirements["isi_articles"]:
            print("- Trebuie să aibă cel puțin 2 articole ISI.")
        if not requirements["cumulative_impact_factor"]:
            print("- Trebuie să aibă un factor de impact cumulat de cel puțin 1.5.")
        if not requirements["student_first_author"]:
            print("- Trebuie să fie prim autor la cel puțin un articol.")
        if not requirements["coordinator_co_author"]:
            print("- Coordonatorul trebuie să fie co-autor la cel puțin un articol.")


"""Add a function to let use pick a  valid ID"""


def get_student_id(config: dict) -> int:
    while True:
        try:
            student_id = int(input("Introduceți ID-ul studentului: "))
            if stud_db.student_id_exists(config, student_id):
                return student_id
            else:
                print("ID-ul introdus nu există în baza de date. Vă rugăm să introduceți un ID valid.")
        except ValueError:
            print("Vă rugăm să introduceți un număr valid.")

if __name__ == '__main__':
    config = db.read_config()
    isi_resources = get_isi_resources('isi_db.json')
    student_id = get_student_id(config)
    requirements = check_graduation_requirements(config, student_id, isi_resources)
    print_graduation_status(student_id, requirements)
