# ═══════════════════════════════════════════════════════════════
#  Flask Student Portal — Deployment Documentation
# ═══════════════════════════════════════════════════════════════
#
#  LOCAL EXECUTION
#  ───────────────
#  1. Install dependencies:
#       pip install flask
#  2. Run the application:
#       python 11_Flask_Application_Deployment.py
#  3. Open in browser:
#       http://127.0.0.1:5001
#
#  PRODUCTION DEPLOYMENT (Render / PythonAnywhere)
#  ────────────────────────────────────────────────
#  A. Create requirements.txt:
#       flask
#       gunicorn
#
#  B. Create a Procfile (for Render / Heroku):
#       web: gunicorn 11_Flask_Application_Deployment:app
#
#  C. Deploy on Render (https://render.com):
#       - Create a new Web Service → connect your GitHub repo
#       - Build command:  pip install -r requirements.txt
#       - Start command:  gunicorn 11_Flask_Application_Deployment:app
#       - The service URL will be: https://<app-name>.onrender.com
#
#  D. Deploy on PythonAnywhere (https://www.pythonanywhere.com):
#       - Upload files → open a Bash console
#       - pip install flask
#       - In the Web tab, set the WSGI file to import `app`
#         from 11_Flask_Application_Deployment
#       - The URL will be: https://<username>.pythonanywhere.com
#
#  IMPORTANT: Set debug=False in production.
# ═══════════════════════════════════════════════════════════════

from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

students = []

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Student Portal</title></head>
<body>
    <h1>Student Portal</h1>
    <nav>
        <a href="/">Home</a> |
        <a href="/register">Register</a> |
        <a href="/students">View Students</a> |
        <a href="/about">About</a>
    </nav>
    <hr>
    <p>Welcome to the Student Portal. Use the navigation to explore.</p>
</body>
</html>
"""

REGISTER_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Register Student</title></head>
<body>
    <h1>Register Student</h1>
    <nav>
        <a href="/">Home</a> |
        <a href="/register">Register</a> |
        <a href="/students">View Students</a> |
        <a href="/about">About</a>
    </nav>
    <hr>
    <form method="POST" action="/register">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>
        <label>Course:</label><br>
        <input type="text" name="course" required><br><br>
        <button type="submit">Register</button>
    </form>
</body>
</html>
"""

STUDENTS_PAGE = """
<!DOCTYPE html>
<html>
<head><title>All Students</title></head>
<body>
    <h1>Registered Students</h1>
    <nav>
        <a href="/">Home</a> |
        <a href="/register">Register</a> |
        <a href="/students">View Students</a> |
        <a href="/about">About</a>
    </nav>
    <hr>
    {% if students %}
    <table border="1" cellpadding="8">
        <tr><th>Name</th><th>Email</th><th>Course</th></tr>
        {% for s in students %}
        <tr><td>{{ s.name }}</td><td>{{ s.email }}</td><td>{{ s.course }}</td></tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No students registered yet.</p>
    {% endif %}
</body>
</html>
"""

ABOUT_PAGE = """
<!DOCTYPE html>
<html>
<head><title>About</title></head>
<body>
    <h1>About</h1>
    <nav>
        <a href="/">Home</a> |
        <a href="/register">Register</a> |
        <a href="/students">View Students</a> |
        <a href="/about">About</a>
    </nav>
    <hr>
    <p>Student Portal built using Flask.</p>
    <p>Developer: Tanishq Saini | Course: BCA</p>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HOME_PAGE)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"]
        }
        students.append(student)
        return redirect(url_for("view_students"))
    return render_template_string(REGISTER_PAGE)


@app.route("/students")
def view_students():
    return render_template_string(STUDENTS_PAGE, students=students)


@app.route("/about")
def about():
    return render_template_string(ABOUT_PAGE)


if __name__ == "__main__":
    app.run()
