-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

-- Books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR
);


INSERT INTO users (username, password)
VALUES
('admin', 'scrypt:32768:8:1$UqI0mYqsUUBUu62e$721c4855d3dca3b96e4e28cf6af8a43c43925210bad31803bd7b5e622babcb0e51bd7154e7bb59558e3ea3684035d7ec4eac0d82644a013e704f2d2486a129d6'),
('karoll_books', 'scrypt:32768:8:1$YqBbti0JnFnH5s4S$36abf326bef255f24b7a5383752811a9d66de1a8d89fe95c79dadc6b7dd19f274c4d6dc976a9b7866509d0457568012f3e68cfb45b2b514da78012e7d51ebeef');

