from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "abc123"


# Database Create
def create_database():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # Banner table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banners(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_url TEXT,
        title TEXT,
        description TEXT
    )
    """)

    # Vision & Mission table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vision_mission(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vision_title TEXT,
        vision_description TEXT,
        mission_title TEXT,
        mission_description TEXT
    )
    """)

    # Statistics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS statistics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT,
        value TEXT
    )
    """)

    # Initiatives table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS initiatives(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    )
    """)
    # About Us Tables

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS our_story(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_values(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS programs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_members(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            image_url TEXT
    
    )
    """)
    

    conn.commit()
    conn.close()



create_database()


@app.route("/")
def home():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM banners")
    banners = cursor.fetchall()

    cursor.execute("SELECT * FROM vision_mission")
    vision_data = cursor.fetchall()

    cursor.execute("SELECT * FROM statistics")
    statistics = cursor.fetchall()

    cursor.execute("SELECT * FROM initiatives")
    initiatives = cursor.fetchall()

    conn.close()

    return render_template(
        "home.html",
        banners=banners,
        vision_data=vision_data,
        statistics=statistics,
        initiatives=initiatives
    )


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    message = ""

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            message = "Email already registered"

            return render_template(
                'register.html',
                message=message
            )

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template(
        'register.html',
        message=message
    )


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session['name'] = user[1]
            return redirect('/dashboard')

        else:
            message = "Invalid Email or Password"

            return render_template(
                'login.html',
                message=message
            )

    return render_template(
        'login.html',
        message=""
    )


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'name' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        name=session['name']
    )

# Manage Banner
@app.route('/manage-banner', methods=['GET', 'POST'])
def manage_banner():

    if 'name' not in session:
        return redirect('/login')

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        image_url = request.form['image_url']
        title = request.form['title']
        description = request.form['description']

        cursor.execute(
            """
            INSERT INTO banners
            (image_url, title, description)
            VALUES (?, ?, ?)
            """,
            (
                image_url,
                title,
                description
            )
        )

        conn.commit()

    cursor.execute("SELECT * FROM banners")
    banners = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_banner.html",
        banners=banners
    )


# Manage Vision
@app.route('/manage-vision', methods=['GET', 'POST'])
def manage_vision():

    if 'name' not in session:
        return redirect('/login')

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        vision_title = request.form['vision_title']
        vision_description = request.form['vision_description']
        mission_title = request.form['mission_title']
        mission_description = request.form['mission_description']

        cursor.execute(
            """
            INSERT INTO vision_mission
            (
                vision_title,
                vision_description,
                mission_title,
                mission_description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                vision_title,
                vision_description,
                mission_title,
                mission_description
            )
        )

        conn.commit()

    cursor.execute("SELECT * FROM vision_mission")
    vision_data = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_vision.html",
        vision_data=vision_data
    )


# Manage Statistics
@app.route('/manage-statistics', methods=['GET', 'POST'])
def manage_statistics():

    if 'name' not in session:
        return redirect('/login')

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        label = request.form['label']
        value = request.form['value']

        cursor.execute(
            "INSERT INTO statistics(label, value) VALUES (?, ?)",
            (label, value)
        )

        conn.commit()

    cursor.execute("SELECT * FROM statistics")
    statistics = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_statistics.html",
        statistics=statistics
    )


# Manage Initiatives
@app.route('/manage-initiatives', methods=['GET', 'POST'])
def manage_initiatives():

    if 'name' not in session:
        return redirect('/login')

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']

        cursor.execute(
            """
            INSERT INTO initiatives
            (title, description)
            VALUES (?, ?)
            """,
            (
                title,
                description
            )
        )

        conn.commit()

    cursor.execute("SELECT * FROM initiatives")
    initiatives = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_initiatives.html",
        initiatives=initiatives
    ) 


@app.route("/manage_story")
def manage_story():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM our_story")
    stories = cursor.fetchall()

    conn.close()
    return render_template("manage_story.html", stories=stories)


@app.route("/manage_core_values")
def manage_core_values():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM core_values")
    values = cursor.fetchall()

    conn.close()
    return render_template("manage_core_values.html", values=values)


@app.route("/manage_programs")
def manage_programs():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    conn.close()
    return render_template("manage_programs.html", programs=programs)


@app.route("/manage_team")
def manage_team():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM team_members")
    team = cursor.fetchall()

    conn.close()
    return render_template("manage_team.html", team=team)    


# Delete Banner
@app.route('/delete-banner/<int:id>')
def delete_banner(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM banners WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage-banner')


# Delete Vision
@app.route('/delete-vision/<int:id>')
def delete_vision(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM vision_mission WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage-vision')


# Delete Statistics
@app.route('/delete-statistics/<int:id>')
def delete_statistics(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM statistics WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage-statistics')


# Delete Initiative
@app.route('/delete-initiative/<int:id>')
def delete_initiative(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM initiatives WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/manage-initiatives')


@app.route("/add_story", methods=["POST"])
def add_story():
    content = request.form["content"]

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO our_story (content) VALUES (?)",
        (content,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_story")


@app.route("/delete_story/<int:id>")
def delete_story(id):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM our_story WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_story")    
    
@app.route("/add_core_value", methods=["POST"])
def add_core_value():
    value = request.form["value"]

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO core_values (value) VALUES (?)",
        (value,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_core_values")


@app.route("/delete_core_value/<int:id>")
def delete_core_value(id):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM core_values WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_core_values")

@app.route("/add_program", methods=["POST"])
def add_program():

    name = request.form["name"]
    description = request.form["description"]

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO programs (name, description) VALUES (?, ?)",
        (name, description)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_programs")


@app.route("/delete_program/<int:id>")
def delete_program(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM programs WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_programs")    

@app.route("/add_team_member", methods=["POST"])
def add_team_member():

    name = request.form["name"]
    role = request.form["role"]

    image = request.files["image"]

    filename = secure_filename(image.filename)

    image.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO team_members
        (name, role, image_url)
        VALUES (?, ?, ?)
        """,
        (name, role, filename)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_team")


@app.route("/delete_team_member/<int:id>")
def delete_team_member(id):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM team_members WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/manage_team")    

@app.route("/about")
def about():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM our_story")
    stories = cursor.fetchall()

    cursor.execute("SELECT * FROM core_values")
    values = cursor.fetchall()

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    cursor.execute("SELECT * FROM team_members")
    team = cursor.fetchall()

    conn.close()

    return render_template(
        "about.html",
        stories=stories,
        values=values,
        programs=programs,
        team=team
    )

    
# Logout
@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        debug=True
    )