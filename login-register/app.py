from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "abc123"

# Create database table
def create_database():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


create_database()


# Home Page
@app.route('/')
def home():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():

    message = ""

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        # Check email exists
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

        # Insert new user
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


# Login Page
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
            return render_template("dashboard.html", name=user[1])
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

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/login')

    
import os

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
