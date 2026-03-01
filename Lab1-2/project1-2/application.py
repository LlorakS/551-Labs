import os
import json
from flask import Flask, session, render_template, request, redirect, url_for, flash,jsonify, Response
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


# ==========================================
# 1. FIX DATABASE URL SILENTLY
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set")


if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-key-for-dev")
Session(app)

# Set up database
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))


# ==========================================
# ROUTES
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
        # Get book
        book_data = db.execute(
            text("SELECT id, isbn, title, author, year FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}
        ).mappings().fetchone()

        if not book_data:
            flash("Book not found.", "warning")
            return redirect(url_for("search"))

        # Get reviews
        reviews = db.execute(
            text("""
                SELECT users.username, reviews.rating, reviews.review
                FROM reviews
                JOIN users ON reviews.user_id = users.id
                WHERE reviews.book_id = :book_id
            """),
            {"book_id": book_data["id"]}
        ).mappings().fetchall()

        # Google Books API #
        import requests
        res = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": f"isbn:{isbn}"}
        )
        print(res.json())

        data = res.json()

        average_rating = None
        ratings_count = None
        description = None

        if data.get("totalItems", 0) > 0:
            volume = data["items"][0]["volumeInfo"]
            average_rating = volume.get("averageRating")
            ratings_count = volume.get("ratingsCount")
            description = volume.get("description")

        return render_template(
            "book.html",
            book=book_data,
            reviews=reviews,
            average_rating=average_rating,
            ratings_count=ratings_count,
            description=description
        )

    except Exception as e:
        db.rollback()
        flash("You have already submitted a review for this book!", "danger")
        return redirect(url_for("book", isbn=isbn))    



# ----- Review Page -----
@app.route("/review/<isbn>", methods=["POST"])
def submit_review(isbn):

    if "user_id" not in session:
        return redirect(url_for("login"))

    rating = request.form.get("rating")
    review_text = request.form.get("review")

    try:
        # Get book id properly
        book = db.execute(
            text("SELECT id FROM books WHERE isbn = :isbn"),
            {"isbn": isbn}
        ).mappings().fetchone()

        if not book:
            return "Book not found", 404

        # Insert review 
        db.execute(
            text("""
                INSERT INTO reviews (user_id, book_id, rating, review)
                VALUES (:user_id, :book_id, :rating, :review)
            """),
            {
                "user_id": session["user_id"],
                "book_id": book["id"],
                "rating": rating,
                "review": review_text
            }
        )

        db.commit()

    except Exception as e:
        db.rollback()
        flash("You have already submitted a review for this book.", "danger")
        return redirect(url_for("book", isbn=isbn))


# ------ API route ------
@app.route("/api/<string:isbn>")
def api_book(isbn):

    book = db.execute(
        text("""
            SELECT isbn, title, author, year
            FROM books
            WHERE isbn = :isbn
        """),
        {"isbn": isbn}
    ).mappings().fetchone()

    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Get review statistics
    stats = db.execute(
        text("""
            SELECT COUNT(*) AS review_count,
                   AVG(rating) AS average_score
            FROM reviews
            JOIN books ON reviews.book_id = books.id
            WHERE books.isbn = :isbn
        """),
        {"isbn": isbn}
    ).mappings().fetchone()

    # 🔥 Google Books API call (ADD THIS PART)
    import requests
    res = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": f"isbn:{isbn}"}
    )

    data = res.json()
    description = None

    if data.get("totalItems", 0) > 0:
        volume = data["items"][0]["volumeInfo"]
        description = volume.get("description")

    # Return JSON response
    response = Response(
        json.dumps({
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "isbn": book["isbn"],
            "review_count": stats["review_count"],
            "average_score": float(stats["average_score"]) if stats["average_score"] else 0,
            "description": description   # 🔥 Added here
        }, indent=4),
        mimetype="application/json"
    )

    return response







if __name__ == "__main__":
    app.run(debug=True)