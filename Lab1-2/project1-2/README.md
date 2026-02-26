# Project 1 ~ Book Review Application

ENGO 551

A Flask-based web app that allows users to register, log in, search through a database of thousands of books, view book summaries, and submit reviews. This application stores user information, book data, as well as reviwes in the PostgreSQL database.
The application integrates the Google Books API to retrieve external rating information for any book (given google contains book information). An API endpioint is also impoletments to allow access to book data in Json format.

## Features
- User registration and login system
- Secure password hashing
- Book search by title, author, or ISBN
- Individual book detail pages
- Submit and view user reviews
- Prevent duplicate reviews per user per book
- Google Books API integration (external ratings)
- JSON API endpoint (`/api/<isbn>`)

## File Structure
**application.py**: The core Flask application logic. It handles user authentication (registration/login), session management, and the search functionality using SQLAlchemy to query the PostgreSQL database.
**import.py**: A standalone Python script used to migrate data from `books.csv` into the SQL database. It handles CSV parsing and batch inserts while ensuring SQLAlchemy compatibility.
**books.csv**: The source data file containing ISBNs, titles, authors, and publication years for 5,000 books.
**templates/**: Contains the Jinja2 HTML templates:
    * `layout.html`: The base template containing the Bootstrap 4 CDN, navigation bar, and flash message logic.
    * `login.html` & `register.html`: User authentication forms.
    * `search.html`: The main dashboard where users query the book database.
    * `book.html`: A detail page displaying specific information for a selected book.
**static/**: Contains CSS and images (logo and background) to provide a clean, modern user interface.

# Features
**Secure Authentication**: Uses `werkzeug.security` to hash passwords before storing them, ensuring no plain-text passwords exist in the database.
**Case-Insensitive Search**: Implements the `ILIKE` operator in SQL to allow flexible searching.
**Session Management**: Uses `flask_session` to store user data server-side, providing a more secure experience than standard client-side cookies.

# How to Run
1.  **Install dependencies**: `pip install -r requirements.txt`
2.  **Set Environment Variables**:
    * `DATABASE_URL`: Your PostgreSQL connection string.
3.  **Import Data**: Run `python import.py` to populate the database.
4.  **Launch App**: Run `flask run` or `python application.py`.