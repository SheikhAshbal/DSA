-- Reuse the Lesson 2 schema and data. For a fresh database, run
-- lesson02-setup.sql first. Run this file once to define the views.
-- All definitions are additive: no existing tables or views are dropped.

-- Q1: Above the overall enrolment average (73.8).
SELECT s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score > (SELECT AVG(score) FROM enrolments)
ORDER BY e.score DESC, e.id ASC;

-- A normal view stores this query definition, not its result rows.
CREATE VIEW passing AS
SELECT e.id AS enrolment_id, s.id AS student_id,
       s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score >= 60;

-- Q2: Passing enrolments per course.
SELECT course, COUNT(*) AS n_passing
FROM passing
GROUP BY course
ORDER BY course;

-- Q3: Top two passing enrolments.
SELECT name, course, score
FROM passing
ORDER BY score DESC, enrolment_id ASC
LIMIT 2;

CREATE INDEX IF NOT EXISTS idx_enrol_student ON enrolments(student_id);

-- Q4: Inspect the plan; exact wording can vary with SQLite versions.
EXPLAIN QUERY PLAN
SELECT * FROM enrolments WHERE student_id = 1;

-- Each eligible student has equal weight in their batch benchmark.
-- Students without any known scores are absent from the benchmark.
CREATE VIEW above_batch_students AS
WITH student_averages AS (
    SELECT s.id AS student_id, s.name, s.batch,
           AVG(e.score) AS student_avg
    FROM students AS s
    JOIN enrolments AS e ON e.student_id = s.id
    WHERE e.score IS NOT NULL
    GROUP BY s.id, s.name, s.batch
),
batch_averages AS (
    SELECT batch, AVG(student_avg) AS batch_avg
    FROM student_averages
    GROUP BY batch
)
SELECT sa.student_id, sa.name, sa.batch, sa.student_avg, ba.batch_avg
FROM student_averages AS sa
JOIN batch_averages AS ba ON ba.batch = sa.batch
WHERE sa.student_avg > ba.batch_avg;

-- Q5: Weekly report; the view does not schedule it automatically.
SELECT student_id, name, batch, student_avg, batch_avg
FROM above_batch_students
ORDER BY batch, student_avg DESC, student_id ASC;
