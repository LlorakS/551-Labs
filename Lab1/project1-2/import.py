import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database setup
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Open CSV and insert into database
with open("books.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": row["isbn"], "title": row["title"], "author": row["author"], "year": row["year"]})
db.commit()
print("Books imported successfully!")
