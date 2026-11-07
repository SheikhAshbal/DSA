# Lesson 2: SQL Basics — SELECT, WHERE, JOIN, GROUP BY, ORDER BY

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-01-Relational-Databases-and-Relational-Algebra.md)

**Course:** Data Science and Analytics  
**Module IV:** Review of Relational Algebra and SQL  
**Estimated study time:** 60 minutes

## Learning objectives

- Filter rows with WHERE and choose output columns with SELECT.
- Join related tables to answer cross-table questions.
- Summarise groups using aggregate functions.
- Distinguish WHERE from HAVING.
- Rank and limit results predictably.
- Debug queries using logical evaluation order.

## 1. The written query skeleton

A common query follows this written order:

```text
SELECT   output_columns
FROM     source_table
JOIN     related_table ON join_condition
WHERE    row_condition
GROUP BY grouping_columns
HAVING   group_condition
ORDER BY sort_expressions
LIMIT    number_of_rows;
```

Optional clauses are included only when needed.

### Seven clause groups

The lesson asks for seven core clauses. Count FROM and its JOIN expressions together as the source clause:

| Written position | Clause | Main job |
| --- | --- | --- |
| 1 | SELECT | Choose the output columns or expressions |
| 2 | FROM, including JOIN ... ON | Identify and combine source tables |
| 3 | WHERE | Filter individual input rows |
| 4 | GROUP BY | Form groups sharing grouping values |
| 5 | HAVING | Filter groups |
| 6 | ORDER BY | Sort the result |
| 7 | LIMIT | Keep a bounded number of result rows |

If JOIN is listed separately, the displayed skeleton has eight entries. This is a counting convention, not a difference in query behaviour.

SELECT corresponds to projection and WHERE to selection from relational algebra. JOIN combines related records. SQL normally retains duplicate output rows unless DISTINCT is requested.

## 2. Aggregation: rows become summaries

GROUP BY assigns input rows to groups with the same grouping values. Aggregate functions calculate a summary for each group.

| Function | Result |
| --- | --- |
| COUNT(*) | Number of input rows |
| COUNT(score) | Number of non-NULL scores |
| AVG(score) | Mean of non-NULL scores |
| SUM(score) | Total of non-NULL scores |
| MIN(score), MAX(score) | Lowest and highest non-NULL scores |

NULL is not zero. A group containing rows but no known scores has COUNT(*) greater than zero and COUNT(score) equal to zero; AVG(score) is NULL.

For the supplied five enrolments:

| Course | Scores | Count | Mean |
| --- | --- | ---: | ---: |
| Data Science | 88, 72 | 2 | 80 |
| Security | 91, 55, 63 | 3 | 69.666... |

Grouping returns two summary rows, one per course. It does not select two original enrolments.

In portable grouped queries, output columns should be grouping columns or aggregate expressions, unless a supported functional-dependency rule permits otherwise. SQLite allows some bare-column queries whose chosen values may be ambiguous; avoid relying on that behaviour.

## 3. WHERE versus HAVING

WHERE determines which rows enter the grouping calculation. HAVING determines which completed groups remain.

| Requirement | Clause |
| --- | --- |
| Enrolments with score > 60 | WHERE score > 60 |
| Rows from batch 23BSCYS | WHERE batch = '23BSCYS' |
| Rows whose scores are known | WHERE score IS NOT NULL |
| Courses with mean score > 70 | HAVING AVG(score) > 70 |
| Groups containing at least five rows | HAVING COUNT(*) >= 5 |

A condition on an aggregate of the current query does not belong in WHERE. It cannot filter a group before that group has been formed.

Filtering rows changes the population used in a mean. If you remove low scores with WHERE and then calculate the average, you obtain the average of retained attempts, not the average of all attempts.

HAVING can also reference grouping keys, but simple row predicates are usually clearer in WHERE. The central distinction is the level and timing of the condition.

## 4. Logical evaluation order

For this lesson's simple query structure:

```text
FROM / JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

This is a logical reasoning model. The database optimiser can choose a physical plan that avoids literally performing each step in that sequence while preserving the result.

### Output aliases

An alias such as AVG(score) AS avg_score names an output expression. In portable SQL, a SELECT output alias is not generally available in the same query's WHERE. ORDER BY can use output aliases.

SQLite accepts some nonaggregate aliases in WHERE as an extension. That does not make filtering a current-query aggregate in WHERE valid. For portability, repeat a row-level expression or expose the calculated column through an outer query.

For an aggregate filter, use HAVING AVG(score) >= 70 or calculate the summary in a subquery and filter its result outside.

See the [PostgreSQL SELECT reference](https://www.postgresql.org/docs/current/sql-select.html) for output-name scope and logical processing, and the [SQLite SELECT reference](https://www.sqlite.org/lang_select.html) for SQLite's processing model.

## 5. Practice database and runnable files

This lesson uses its own simplified schema:

```text
students(id, name, batch)
enrolments(id, student_id -> students.id, course, score)
```

Course names and batch codes are stored directly for this small exercise. This is a teaching simplification relative to the separate course and batch tables in Lesson 1.

- [lesson02-setup.sql](./lesson02-setup.sql): creates the tables and inserts three students and five enrolments.
- [lesson02-queries.sql](./lesson02-queries.sql): contains seven queries covering the lesson.

Run setup once in a fresh SQLite database, then run the query file in that same database. Use a separate database from Lesson 1 because the schemas differ.

In PowerShell, with the SQLite CLI installed, run from the directory containing these files:

```powershell
Get-Content -Raw -LiteralPath './lesson02-setup.sql' | sqlite3 dsa-lesson02.db
Get-Content -Raw -LiteralPath './lesson02-queries.sql' | sqlite3 -header -column dsa-lesson02.db
```

Setup returns enrolment_count = 5. It intentionally does not drop existing tables. Choose a new database filename if those tables already exist.

Python includes a sqlite3 module in typical installations, but the separate sqlite3 command-line executable is not guaranteed to be installed with Python. SQLite dot commands such as .headers and .mode belong to the CLI, not SQL submitted through a database API.

## 6. Worked practice

### Practice 1 — Build the database

Run the setup file, which declares student_id as an enforced foreign key and enables SQLite foreign-key checking for that connection.

Confirm:

```sql
SELECT COUNT(*) AS enrolment_count
FROM enrolments;
```

Expected result: 5.

The keys connect enrolments to students. A foreign-key pragma must be enabled on each connection where enforcement is required.

### Practice 2 — Filter and project

```sql
SELECT student_id, course, score
FROM enrolments
WHERE score >= 60
ORDER BY score DESC, id ASC;
```

| student_id | course | score |
| --- | --- | ---: |
| 1 | Security | 91 |
| 1 | Data Science | 88 |
| 2 | Data Science | 72 |
| 2 | Security | 63 |

WHERE performs selection by retaining passing enrolments. SELECT performs projection by choosing three output columns.

ORDER BY requests descending scores; id provides a stable tie-breaker if equal scores appear later. No result order is guaranteed without ORDER BY.

### Practice 3 — Join across tables

```sql
SELECT s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score >= 80
ORDER BY e.score DESC, e.id ASC;
```

| name | course | score |
| --- | --- | ---: |
| Ali | Security | 91 |
| Ali | Data Science | 88 |

Names are stored in students, while scores and course labels are in enrolments. The join connects those facts through the student key. An equivalent lookup or subquery could also retrieve the name; the essential requirement is accessing both related sources.

### Practice 4 — Aggregate and filter groups

```sql
SELECT course, COUNT(*) AS n, ROUND(AVG(score), 1) AS avg_score
FROM enrolments
WHERE score IS NOT NULL
GROUP BY course
HAVING AVG(score) >= 70
ORDER BY avg_score DESC, course ASC;
```

| course | n | avg_score |
| --- | ---: | ---: |
| Data Science | 2 | 80.0 |

WHERE excludes unknown scores before grouping. HAVING excludes the Security group because its unrounded mean is about 69.6667.

AVG already ignores NULL, but the WHERE condition also makes COUNT(*) count only rows with known scores. A missing score does not itself prove that no attempt occurred; interpret that meaning from the data definition.

Filtering on the unrounded average avoids accepting a group merely because its displayed average rounds upward.

### Practice 5 — Debug the aggregate alias

Problematic query, shown for diagnosis only:

```text
SELECT course, AVG(score) AS avg_score
FROM enrolments
WHERE avg_score >= 70
GROUP BY course;
```

The filter concerns a group aggregate, but WHERE operates on rows before grouping. The alias does not turn that aggregate into a row-level value. SQLite rejects this query as aggregate misuse, even though it permits certain other alias references.

Corrected query:

```sql
SELECT course, AVG(score) AS avg_score
FROM enrolments
GROUP BY course
HAVING AVG(score) >= 70
ORDER BY course;
```

Expected result: Data Science, 80.0.

An outer-query alternative is also valid:

```sql
SELECT course, avg_score
FROM (
    SELECT course, AVG(score) AS avg_score
    FROM enrolments
    GROUP BY course
) AS course_summary
WHERE avg_score >= 70
ORDER BY course;
```

Here avg_score is an input column of course_summary, so the outer WHERE can filter it.

### Ranking extension — ORDER BY and LIMIT

```sql
SELECT student_id, course, score
FROM enrolments
WHERE score IS NOT NULL
ORDER BY score DESC, id ASC
LIMIT 2;
```

This returns the Security score 91 and Data Science score 88, both for Ali. These are the top two enrolments, not necessarily two different students.

LIMIT without a suitable ORDER BY does not mean “the best” rows. A deterministic tie-breaker makes a top-N selection repeatable.

## 7. Theory exercises — suggested answers

These are study references. Explain the reasoning in your own words for course submissions.

### Task 1 — SQL clause skeleton identification

The seven clause groups, in written order, are:

1. SELECT
2. FROM, including JOIN ... ON when combining sources
3. WHERE
4. GROUP BY
5. HAVING
6. ORDER BY
7. LIMIT

SELECT chooses the columns or expressions shown in the result. WHERE keeps only individual rows satisfying the specified condition, before any grouping.

Listing JOIN as its own entry produces eight entries in the expanded skeleton; it is part of the source expression in the seven-group version.

### Task 2 — Aggregation logic analysis

GROUP BY puts rows with the same grouping values into a group. The query then produces a summary row for each retained group instead of returning every original row separately.

Aggregate functions calculate the summaries. For example, SUM adds the known values in a group, AVG calculates their mean, and COUNT(*) counts its rows. Grouping enrolments by course can therefore turn five records into two course-level rows.

### Task 3 — WHERE versus HAVING

Use WHERE salary > 50000 to retain qualifying employee rows before grouping. Then group by department and use HAVING COUNT(*) > 10 to keep departments containing more than ten of those qualifying employees.

This counts employees earning over $50,000 within each department, rather than counting all employees first. WHERE filters employees; HAVING filters the resulting departmental groups.

### Task 4 — SQL execution order reasoning

SQL is written with SELECT first, but its logical processing starts with the source rows and WHERE filtering. The SELECT output alias is therefore not generally available as an input-column name to WHERE in the same query.

Use the original row-level expression in WHERE or put the calculated output in a subquery and filter it outside. If the alias represents an aggregate, use an appropriate HAVING condition.

Some databases, including SQLite, allow additional alias references, so the exact error depends on the SQL dialect. The portable rule remains useful.

### Task 5 — Clause sequence mapping

The approximate logical sequence is:

1. FROM and JOIN — obtain and combine the source rows.
2. WHERE — filter individual rows.
3. GROUP BY — form groups and calculate aggregates.
4. HAVING — filter groups.
5. SELECT — produce the output columns and expressions.
6. ORDER BY — sort the result.
7. LIMIT — retain the requested number of rows.

This describes the meaning of the query rather than requiring a particular physical execution plan.

## 8. Quick revision

- SELECT chooses columns; WHERE chooses rows.
- JOIN connects tables through a condition.
- GROUP BY creates group-level results.
- WHERE changes the rows used in aggregates.
- HAVING filters groups using their properties.
- COUNT(*) and COUNT(column) treat NULL differently.
- Use output aliases in ORDER BY; write portable WHERE and HAVING expressions.
- Sort before using LIMIT for a meaningful top-N result.
- Add tie-breakers when a stable order matters.

## Sources

- User-supplied course material: *Data Science and Analytics, Module IV: Review of Relational Algebra and SQL, SQL Basics: SELECT, WHERE, JOIN, GROUP BY, ORDER BY*.
- [SQLite: SELECT](https://www.sqlite.org/lang_select.html) — logical processing and dialect behaviour.
- [PostgreSQL: SELECT](https://www.postgresql.org/docs/current/sql-select.html) — written syntax, output-name scope, and processing model.

Worked responses and clarifying notes were prepared for this repository.

[Previous lesson](./Lesson-01-Relational-Databases-and-Relational-Algebra.md) · [Module overview](./README.md) · [Theory index](../README.md)
