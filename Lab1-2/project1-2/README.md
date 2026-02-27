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
**application.py**: 
This is the main flask application file, containing,
- All routes (to login, register, search, book page, review submission)
- API endpoint
- Google Books API integration
- Database queries

## Templates
Contains all the HTML templates rendered by flask
- `layout.html` – Base layout template
- `login.html` – Login page
- `register.html` – Registration page
- `search.html` – Book search page
- `book.html` – Individual book details page

## static/
Contains CSS or other static files.

**import.py**: A standalone Python script used to migrate data from `books.csv` into the SQL database. It handles CSV parsing and batch inserts while ensuring SQLAlchemy compatibility.
**books.csv**: The source data file containing ISBNs, titles, authors, and publication years for 5,000 books.


## Database Structure

The application uses PostgreSQL with the following main tables:

### users
- id
- username
- password (hashed)

### books
- id
- isbn
- title
- author
- year

### reviews
- id
- user_id
- book_id
- rating
- review


## How To Run
set FLASK_APP=application.py
set FLASK_ENV=development
set DATABASE_URL=postgresql://postgres:SchoolYay121!@localhost:5432/ENG0551_L1
flask run