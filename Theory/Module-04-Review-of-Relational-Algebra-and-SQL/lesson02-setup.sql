-- Lesson 2 fixture: run once in a fresh SQLite database.
-- Use a separate database from Lesson 1: the teaching schema differs.
PRAGMA foreign_keys = ON;

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    batch TEXT NOT NULL
);

CREATE TABLE enrolments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course TEXT NOT NULL,
    score INTEGER CHECK (score BETWEEN 0 AND 100)
);

INSERT INTO students VALUES
    (1, 'Ali', '23BSCYS'),
    (2, 'Sara', '23BSCYS'),
    (3, 'Omar', '22BSCYS');

INSERT INTO enrolments VALUES
    (1, 1, 'Data Science', 88),
    (2, 2, 'Data Science', 72),
    (3, 1, 'Security', 91),
    (4, 3, 'Security', 55),
    (5, 2, 'Security', 63);

SELECT COUNT(*) AS enrolment_count FROM enrolments;
