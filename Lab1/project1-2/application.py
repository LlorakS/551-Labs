import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ==========================================
# 1. FIX DATABASE URL SILENTLY
# ==========================================
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set")

# SQLAlchemy 1.4+ requires "postgresql://" but many hosts provide "postgres://"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key-for-dev")
Session(app)

# Set up database
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))


# ==========================================
# ROUTES
# ==========================================

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("search"))
    return redirect(url_for("login"))


# ----- Registration -----
@app.route("/register", methods=["GET", "POST"])
def register():
    # Clear any stuck database connections
    db.rollback()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Username and password are required.", "warning")
            return render_template("register.html")

        try:
            # 1. Check if username exists
            user = db.execute(
                text("SELECT id FROM users WHERE username = :username"), 
                {"username": username}
            ).mappings().fetchone()
            
            if user:
                flash("Username already exists.", "danger")
                return render_template("register.html")

            # 2. Insert new user
            hashed_password = generate_password_hash(password)
            db.execute(
                text("INSERT INTO users (username, password) VALUES (:username, :password)"),
                {"username": username, "password": hashed_password}
            )
            db.commit()
            
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
            
        except Exception as e:
            db.rollback() 
            print(f"Database Error: {e}")
            flash("An error occurred during registration. Please try again.", "danger")
            return render_template("register.html")
    
    return render_template("register.html")


# ----- Login -----
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear any stuck database connections
    db.rollback()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            # Fetch user as a dictionary mapping
            result = db.execute(
                text("SELECT id, username, password FROM users WHERE username = :username"), 
                {"username": username}
            ).mappings().fetchone()

            # Check if user exists AND password matches
            if result and check_password_hash(result["password"], password):
                session["user_id"] = result["id"]
                session["username"] = result["username"]
                return redirect(url_for("search"))
            else:
                flash("Invalid username or password.", "danger")
                return redirect(url_for("login")) # Redirect clears the POST request
                
        except Exception as e:
            db.rollback()
            print(f"Database Error: {e}")
            flash("A server error occurred. Please try again.", "danger")
            return redirect(url_for("login"))
    
    return render_template("login.html")


# ----- Logout -----
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ----- Search -----
@app.route("/search", methods=["GET", "POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))

    results = []
    if request.method == "POST":
        query = request.form.get("query")
        search_query = f"%{query}%"
        
        try:
            results = db.execute(
                text("""
                SELECT isbn, title, author, year FROM books
                WHERE isbn ILIKE :q OR title ILIKE :q OR author ILIKE :q
                """), 
                {"q": search_query}
            ).mappings().fetchall()
                
            if not results:
                flash("No results found.", "warning")
        except Exception as e:
            db.rollback()
            print(f"Database Error: {e}")
            flash("Error searching database.", "danger")
    
    return render_template("search.html", results=results)


# ----- Book Page -----
@app.route("/book/<string:isbn>")
def book(isbn):
    if "user_id" not in session:
        return redirect(url_for("login"))

    try:
        book_data = db.execute(
            text("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn"), 
            {"isbn": isbn}
        ).mappings().fetchone()

        if not book_data:
            flash("Book not found.", "warning")
            return redirect(url_for("search"))
            
        return render_template("book.html", book=book_data)
        
    except Exception as e:
        db.rollback()
        print(f"Database Error: {e}")
        flash("Error retrieving book details.", "danger")
        return redirect(url_for("search"))


if __name__ == "__main__":
    app.run(debug=True)