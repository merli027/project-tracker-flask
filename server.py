"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template
import hackbright

app = Flask(__name__)

@app.route('/')
def index():

    projects = hackbright.get_all_projects()
    students = hackbright.get_all_students()

    return render_template('homepage.html',
                           projects=projects,
                           students=students)

@app.route('/add_student', methods=["GET", "POST"])
def add_student():

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        github = request.form.get('github')
        hackbright.make_new_student(first_name, last_name, github)
        return render_template('confirmation.html', github=github)
    else:
        return render_template('student_form.html')


@app.route('/search')
def search():

    return render_template('student_search.html')


@app.route('/project')
def project():

    title = request.args.get('title')
    project = hackbright.get_project_by_title(title)
    grades = hackbright.get_grades_by_title(title)

    return render_template('project.html', project=project, grades=grades)


@app.route('/student')
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    return render_template('student_info.html',
                           github=github, first=first, last=last,
                           grades=grades)


if __name__ == '__main__':
    hackbright.connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
