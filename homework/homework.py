from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
students = []


@app.route("/")
def home():
    return redirect(url_for("add_student"))


@app.route("/add", methods=["GET", "POST"])
def add_student():
    error = None

    if request.method == "POST":
        name = request.form.get("name")
        grade = request.form.get("grade")

        if not name or name.strip() == "":
            error = "Username is required."
            return render_template("add.html", error=error, name=name, grade=grade)

        else:
            try:
                grade = int(grade)
                if grade < 0 or grade > 100:
                    error = "Grade must be between 0 and 100."
                    return render_template("add.html", error=error, name=name, grade=grade)
                else:
                    students.append({"name": name, "grade": grade})
                    return redirect("/students")
            except ValueError:
                error = "Grade must be an integer."
            return render_template("add.html", error=error, name=name, grade=grade)
    return render_template("add.html")


@app.route("/students")
def display_students():
    return render_template("students.html", students=students)


@app.route("/summary")
def summary():
    data = {}
    message = None
    if len(students) == 0:
        message = "There are no students."
    else:
        max = 0
        min = 0
        total = len(students)
        average = 0
        for student in students:
            average += student["grade"]
            if student["grade"] > max:
                max = student["grade"]
            if student["grade"] < min:
                min = student["grade"]
        average /= total
        data["max"] = max
        data["min"] = min
        data["average"] = average
        data["total"] = total

    return render_template("summary.html", data=data, message=message)


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
