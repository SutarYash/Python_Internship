from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
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