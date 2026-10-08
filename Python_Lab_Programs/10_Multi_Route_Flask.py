from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Student Portal"


@app.route("/about")
def about():
    return "This is the About Page"


@app.route("/courses")
def courses():
    return "Courses: BCA, BSc, MCA, MSc"


@app.route("/contact")
def contact():
    return "Email: ts@example.com"


@app.route("/profile")
def profile():
    return "Student Name: Tanishq Saini | Course: BCA | Contact: ts@example.com"


@app.route("/subjects")
def subjects():
    return "Subjects: Python, Java, Database Management, Artificial Intelligence"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
