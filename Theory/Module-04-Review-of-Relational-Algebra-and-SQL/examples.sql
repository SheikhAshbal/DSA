-- Module IV, Lesson 1: SQLite-compatible demonstration.
-- Run in a fresh SQLite database. Foreign-key enforcement is connection-specific.
PRAGMA foreign_keys = ON;

CREATE TABLE batches (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    batch_id INTEGER REFERENCES batches(id),
    score INTEGER CHECK (score BETWEEN 0 AND 100)
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    teacher TEXT NOT NULL
);

CREATE TABLE enrolments (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    grade INTEGER CHECK (grade BETWEEN 0 AND 100),
    UNIQUE (student_id, course_id)
);

CREATE TABLE lessons (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id),
    title TEXT NOT NULL
);

CREATE TABLE completions (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id),
    completed_at TEXT NOT NULL,
    UNIQUE (student_id, lesson_id)
);

INSERT INTO batches VALUES (10, '23BSCYS'), (20, '22BSCYS');
INSERT INTO students VALUES
    (1, 'Ali', 10, 88),
    (2, 'Sara', 10, 72),
    (3, 'Omar', NULL, 55);
INSERT INTO courses VALUES
    (101, 'Data Science and Analytics', 'Teacher A'),
    (102, 'Database Foundations', 'Teacher B');
INSERT INTO enrolments VALUES
    (1, 1, 101, 88),
    (2, 2, 101, 72),
    (3, 1, 102, 91);
INSERT INTO lessons VALUES
    (1001, 101, 'Relational Databases and Relational Algebra'),
    (1002, 101, 'Next lesson placeholder');
INSERT INTO completions VALUES
    (1, 1, 1001, '2026-11-07T10:00:00+05:00');

-- Selection followed by projection.
SELECT DISTINCT name
FROM students
WHERE score >= 60
ORDER BY name;

-- An inner join keeps matching students only.
SELECT s.name, b.code
FROM students AS s
INNER JOIN batches AS b ON s.batch_id = b.id
ORDER BY s.id;

-- A left join preserves Omar, whose batch is not assigned.
SELECT s.name, b.code
FROM students AS s
LEFT JOIN batches AS b ON s.batch_id = b.id
ORDER BY s.id;

-- Names of students enrolled in course 101.
SELECT DISTINCT s.name
FROM students AS s
JOIN enrolments AS e ON e.student_id = s.id
WHERE e.course_id = 101
ORDER BY s.name;

-- Union: student IDs enrolled in either course.
SELECT student_id FROM enrolments WHERE course_id = 101
UNION
SELECT student_id FROM enrolments WHERE course_id = 102
ORDER BY student_id;

-- Difference: student IDs in course 101 but not course 102.
SELECT student_id FROM enrolments WHERE course_id = 101
EXCEPT
SELECT student_id FROM enrolments WHERE course_id = 102
ORDER BY student_id;
