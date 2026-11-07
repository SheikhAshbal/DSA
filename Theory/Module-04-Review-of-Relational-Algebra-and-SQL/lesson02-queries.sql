-- Run after lesson02-setup.sql in the same SQLite database.

-- Q1: Passing enrolments, highest score first.
SELECT student_id, course, score
FROM enrolments
WHERE score >= 60
ORDER BY score DESC, id ASC;

-- Q2: Names and scores across the relationship.
SELECT s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score >= 80
ORDER BY e.score DESC, e.id ASC;

-- Q3: Unfiltered course summaries.
SELECT course, COUNT(*) AS n, ROUND(AVG(score), 1) AS avg_score
FROM enrolments
GROUP BY course
ORDER BY course;

-- Q4: Filter rows first, then retain strong groups.
SELECT course, COUNT(*) AS n, ROUND(AVG(score), 1) AS avg_score
FROM enrolments
WHERE score IS NOT NULL
GROUP BY course
HAVING AVG(score) >= 70
ORDER BY avg_score DESC, course ASC;

-- Q5: Correct the aggregate-alias-in-WHERE error.
SELECT course, AVG(score) AS avg_score
FROM enrolments
GROUP BY course
HAVING AVG(score) >= 70
ORDER BY course;

-- Q6: An outer query can filter the computed result as ordinary rows.
SELECT course, avg_score
FROM (
    SELECT course, AVG(score) AS avg_score
    FROM enrolments
    GROUP BY course
) AS course_summary
WHERE avg_score >= 70
ORDER BY course;

-- Q7: Top two enrolments, with a stable tie-breaker.
SELECT student_id, course, score
FROM enrolments
WHERE score IS NOT NULL
ORDER BY score DESC, id ASC
LIMIT 2;
