import csv
import os
from sqlalchemy import create_engine, text # Added text
from sqlalchemy.orm import scoped_session, sessionmaker

# Database setup
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set")

# 1. FIX: Ensure URL is compatible with SQLAlchemy 1.4+
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("books.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.execute(
                text("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)"),
                {"isbn": row["isbn"], "title": row["title"], "author": row["author"], "year": row["year"]}
            )
            print(f"Adding book: {row['title']}") # Progress update
        
        db.commit()
        print("Books imported successfully!")

if __name__ == "__main__":
    main()