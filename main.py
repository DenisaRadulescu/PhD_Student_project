from flask import Flask, render_template, request, redirect, url_for
from auth import login as auth_login, add_user as auth_add_user
import universities_db as uni_db
import professors_db as prof_db
import students_db as stud_db
import connect_to_db as db
import graduation_requirements as grad_req
import os
import json

app = Flask(__name__)

# Path to the credentials file
credentials_path = "auth.json"

# Variable to store the current logged-in user
current_user = None

@app.route('/', methods=['GET', 'POST'])
def index():
    """App route for login/register"""
    global current_user
    form_type = request.args.get('form_type', 'login')

    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')

        if 'login' in request.form and form_type == 'login':
            # Handle login
            if auth_login(username=username, password=password, path=credentials_path):
                current_user = username
                return redirect(url_for('homepage'))
            else:
                return render_template('login.html', message='Login failed. Please check your username and password.', form_type='login')
        elif 'register' in request.form and form_type == 'register':
            # Handle registration
            if password == confirm_password:
                if auth_add_user(username=username, password=password, confirm_password=password, path=credentials_path):
                    return render_template('login.html', message='User registered successfully! Please log in.', form_type='login')
                else:
                    return render_template('login.html', message='Registration failed: username already exists or '
                                                                 'password criteria not met: '
                                                                 '6 characters from which one capslock letter, '
                                                                 'one number and one special character.', form_type='register')
            else:
                return render_template('login.html', message='Passwords do not match.', form_type='register')

    return render_template('login.html', form_type=form_type)

def is_admin():
    """Check if the current user is an admin"""
    return current_user == "admin"


@app.route('/logout')
def logout():
    """Logout option"""
    global current_user
    current_user = None
    return redirect(url_for('index'))


@app.route('/homepage', methods=['GET'])
def homepage():
    """App route for homepage"""
    return render_template('homepage.html', content="Welcome to the Dashboard!")


@app.route('/show_universities')
def show_universities():
    """Show universities on the homepage"""
    config = db.read_config()
    universities = uni_db.select_universities_from_db(config)
    content = "<h2>Universities List</h2><ul>"
    for uni in universities:
        content += f"<li>{uni.get('university_id')}. {uni.get('faculty_name')}</li>"
    content += "</ul>"
    return render_template('homepage.html', content=content)


@app.route('/add_university', methods=['GET', 'POST'])
def add_university():
    """Add a university on the homepage"""

    # Restricts access for only admin
    if not is_admin():
        return render_template('homepage.html', content="Access denied. Admin rights required.")

    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        config = db.read_config()

        success, message = uni_db.add_university_to_db(config, faculty_name)

        return render_template('homepage.html', content=message)

    return render_template('homepage.html', content=render_template('add_university_form.html'))


@app.route('/show_professors')
def show_professors():
    """Show professors on the homepage"""
    config = db.read_config()
    professors = prof_db.select_professors_from_db(config)
    content = "<h2>Professors List</h2><ul>"
    for prof in professors:
        content += f"<li>{prof.get('professor_id')}. {prof.get('title')} {prof.get('name')} - {prof.get('faculty_name')}</li>"
    content += "</ul>"
    return render_template('homepage.html', content=content)


@app.route('/add_professor', methods=['GET', 'POST'])
def add_professor():
    """Add a professor to the database"""

    # Restricts access for only admin
    if not is_admin():
        return render_template('homepage.html', content="Access denied. Admin rights required.")

    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        university_id = request.form['university_id']

        config = db.read_config()

        success, message = prof_db.add_professor_to_db(config, title, name, int(university_id))
        print(f"Add Professor Result: Success: {success}, Message: {message}")
        return render_template('homepage.html', content=message)

    return render_template('homepage.html', content=render_template('add_professor_form.html'))



@app.route('/show_students')
def show_students():
    """Show students on the homepage with all available information including university name"""
    config = db.read_config()
    students = stud_db.select_all_students(config)
    return render_template('homepage.html', content=render_template('students_table.html', students=students))


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add a student to the database"""

    # Restricts access for only admin
    if not is_admin():
        return render_template('homepage.html', content="Access denied. Admin rights required.")

    if request.method == 'POST':
        name = request.form['name']
        funding_type = request.form['funding_type']
        scholarship = request.form['scholarship']
        university_id = request.form['university_id']

        config = db.read_config()

        success, message = stud_db.add_student_to_db(config, name, funding_type, scholarship, int(university_id))
        print(f"Add Student Result: Success: {success}, Message: {message}")
        return render_template('homepage.html', content=message)

    return render_template('homepage.html', content=render_template('add_student_form.html'))


@app.route('/show_all_articles')
def show_all_articles():
    """Show all articles on the homepage"""
    config = db.read_config()
    articles = stud_db.select_articles_from_db(config)
    return render_template('homepage.html', content=render_template('articles_table.html', articles=articles))


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    """Add an article to the database"""

    # Restricts access for only admin
    if not is_admin():
        return render_template('homepage.html', content="Access denied. Admin rights required.")

    if request.method == 'POST':
        config = db.read_config()
        success, message = stud_db.add_article_to_db(config, **request.form)
        return render_template('homepage.html', content=message)
    return render_template('homepage.html', content=render_template('add_article_form.html'))


@app.route('/check_graduation_requirements', methods=['GET', 'POST'])
def check_graduation_requirements():
    """Check if a student meets graduation requirements"""
    config = db.read_config()

    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        isi_resources = grad_req.get_isi_resources('isi_db.json')
        requirements = grad_req.check_graduation_requirements(config, student_id, isi_resources)

        content = f"<h2>Graduation Requirements Check for Student ID: {student_id}</h2>"
        if all(requirements.values()):
            content += """
                <p>The student has met all graduation requirements.</p>
                <img src="/static/requirements_met.jpg" alt="Graduation Success" style="width:500px;">
            """
        else:
            content += """
                <p>The student has not met all graduation requirements. Details:</p>
                <ul>
            """
            if not requirements["isi_articles"]:
                content += "<li>Needs at least 2 ISI articles.</li>"
            if not requirements["cumulative_impact_factor"]:
                content += "<li>Needs a cumulative impact factor of at least 1.5.</li>"
            if not requirements["student_first_author"]:
                content += "<li>Needs to be first author on at least one article.</li>"
            if not requirements["coordinator_co_author"]:
                content += "<li>Needs the coordinator to be co-author on at least one article.</li>"
            content += """
                </ul>
                <img src="/static/requirements_not_met.jpg" alt="Graduation Incomplete" style="width:600px;">
            """

        return render_template('homepage.html', content=content)

    # If it's a GET request, show the form to input student ID
    students = stud_db.select_all_students(config)
    options = "".join([f'<option value="{s["student_id"]}">{s["student_id"]} - {s["name"]}</option>' for s in students])

    content = f'''
        <h2>Check Graduation Requirements</h2>
        <form method="POST">
            <label for="student_id">Select Student:</label>
            <select id="student_id" name="student_id" required>
                {options}
            </select>
            <button type="submit">Check Requirements</button>
        </form>
    '''
    return render_template('homepage.html', content=content)


if __name__ == '__main__':
    if not os.path.exists(credentials_path):
        # Create the file if it does not exist
        with open(credentials_path, 'w') as f:
            json.dump({}, f)
    app.run(debug=True)
