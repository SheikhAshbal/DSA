# Module IV: Review of Relational Algebra and SQL

[Back to Theory](../README.md)

This module reviews relational databases, SQL querying, and reusable analytical extraction. All three lessons are documented below.

## Lessons

| Lesson | Topic | Repository material |
| --- | --- | --- |
| 1 | [Relational Databases and Relational Algebra](./Lesson-01-Relational-Databases-and-Relational-Algebra.md) | Notes, five worked practice steps, five suggested theory answers, and runnable SQL |
| 2 | [SQL Basics: SELECT, WHERE, JOIN, GROUP BY, ORDER BY](./Lesson-02-SQL-Basics.md) | Notes, five worked practice steps, five suggested theory answers, and verified SQL |
| 3 | [Subqueries, Views and Indexes](./Lesson-03-Subqueries-Views-and-Indexes.md) | Notes, five worked practice steps, five suggested theory answers, and verified SQL |

## Learning objectives

- Identify relations, keys, and relationships.
- Explain normalisation and data anomalies.
- Map relational-algebra operations to SQL.
- Predict join and set-operation results.
- Design and constrain a lesson-completion schema.
- Filter, join, aggregate, rank, and limit query results.
- Distinguish WHERE from HAVING and reason about logical evaluation order.
- Compose subqueries and views for reusable reports.
- Evaluate index benefits, write costs, and query plans.

## SQL examples

Run [examples.sql](./examples.sql) in a fresh SQLite database. It includes sample data, joins, projection, union, and difference.

Lesson 2 uses a separate teaching schema: run [lesson02-setup.sql](./lesson02-setup.sql) once in a fresh database, then [lesson02-queries.sql](./lesson02-queries.sql) in that same database. See the lesson for PowerShell commands.

Lesson 3 reuses the Lesson 2 fixture. Run [lesson03-queries.sql](./lesson03-queries.sql) once to create its views and index, then query the views for later reports.

Repository availability describes documented material, not course grades or submission status.
