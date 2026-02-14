
import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)  # Needed for session
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# ====================
# ROUTES
# ====================

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("search"))
    return redirect(url_for("login"))


# ----- Registration -----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Username and password are required.")
            return render_template("register.html")

        # Check if username exists
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user:
            flash("Username already exists.")
            return render_template("register.html")

        # Insert user into database
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": hashed_password})
        db.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    
    return render_template("register.html")


# ----- Login -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("search"))
        else:
            flash("Invalid username or password.")
            return render_template("login.html")
    
    return render_template("login.html")


# ----- Logout -----
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


# ----- Search -----
@app.route("/search", methods=["GET", "POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))

    results = []
    if request.method == "POST":
        query = request.form.get("query")
        query = f"%{query}%"
        results = db.execute("""
            SELECT * FROM books
            WHERE isbn ILIKE :q OR title ILIKE :q OR author ILIKE :q
            """, {"q": query}).fetchall()
        if not results:
            flash("No results found.")
    
    return render_template("search.html", results=results)


# ----- Book Page -----
@app.route("/book/<string:isbn>")
def book(isbn):
    if "user_id" not in session:
        return redirect(url_for("login"))

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if not book:
        flash("Book not found.")
        return redirect(url_for("search"))
    
    return render_template("book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)




# import os

# from flask import Flask, session
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


# @app.route("/")
# def index():
#     return "Project 1: TODO"
