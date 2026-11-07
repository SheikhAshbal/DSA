# Lesson 1: Relational Databases and Relational Algebra

[Theory index](../README.md) · [Module overview](./README.md)

**Course:** Data Science and Analytics  
**Module IV:** Review of Relational Algebra and SQL  
**Estimated study time:** 45 minutes

## Learning objectives

- Define relations, tuples, attributes, primary keys, and foreign keys.
- Explain why related tables reduce redundancy and update anomalies.
- Identify selection, projection, join, union, difference, and rename.
- Translate simple relational-algebra expressions into SQL.
- Predict inner-join and left-join results.
- Design a schema for student lesson completions.

## 1. The relational model

A relational database organises data into tables connected through keys.

| Term | Meaning |
| --- | --- |
| Relation | In classical relational theory, a set of tuples sharing a schema |
| Tuple | One row or record |
| Attribute | A named field or column |
| Primary key | A column or combination of columns identifying each row uniquely |
| Foreign key | Columns constrained to reference an eligible key in a referenced table |

A primary key is unique and non-null. A foreign key enforces referential integrity: a non-null reference must match a referenced key. A nullable foreign key can represent an optional relationship; use `NOT NULL` when the relationship is mandatory.

Foreign keys can reference qualifying unique keys, not only primary keys, and can refer to the same table. The course's examples use primary keys in other tables.

### Relations and practical SQL tables

Classical relations have no duplicate tuples and no intrinsic row order. SQL permits duplicates in tables without suitable constraints and normally retains duplicates in query output. Use `DISTINCT` when set-style duplicate elimination is required, and `ORDER BY` when output order matters.

Types and constraints improve data integrity, but a database is not automatically correct: a valid integer can still be the wrong score.

## 2. Why split data across tables?

Normalisation organises relations according to their dependencies to reduce unnecessary redundancy and avoid anomalies. This lesson focuses on the practical idea of storing each fact in the appropriate place.

Suppose every enrolment stores a student's name and batch together with a course title and teacher. A name repeated across many enrolments must be updated repeatedly. Missing one copy produces a contradiction.

| Anomaly | Problem in one large enrolment table | Better location |
| --- | --- | --- |
| Update | A name change requires editing many rows | Student name in students |
| Insertion | A new course cannot be recorded without an enrolment, unless incomplete placeholder rows are introduced | Course details in courses |
| Deletion | Deleting the final enrolment may erase the only course details | Keep courses independently |
| Contradiction | Copies of a course disagree about its teacher | One authoritative course record, under the stated teaching model |

Separate student, course, and enrolment tables let an enrolment record the relationship and its grade. Foreign keys prevent dangling references when enforced; they do not automatically repair every semantic inconsistency.

Normalisation is based on dependencies and requirements, not simply splitting every column into its own table. For example, if teachers vary by term or section, model course offerings rather than assuming one teacher per course forever.

## 3. Core relational-algebra operations

| Operation | Symbol | Result | SQL counterpart |
| --- | --- | --- | --- |
| Selection | σ | Rows satisfying a predicate | WHERE |
| Projection | π | Chosen attributes; duplicate tuples removed in classical algebra | SELECT DISTINCT columns |
| Join | ⋈ | Tuples combined where a join predicate matches | JOIN ... ON |
| Union | ∪ | Tuples present in either compatible relation | UNION |
| Difference | − | Tuples in the first relation but not the second | EXCEPT |
| Rename | ρ | A relation or its attributes under new names | Table / column aliases |

**Selection chooses rows; projection chooses columns.** SQL's keyword `SELECT` introduces the column list, so its name can be confusing when learning algebra.

Union and difference require compatible schemas: the same number of attributes with compatible corresponding domains or types. Union removes duplicate tuples. Difference is directional: A − B generally differs from B − A. SQL's `UNION ALL` preserves duplicates instead of performing classical set union.

### Example: passing student names

Assume this teaching example has a score attribute in students:

```text
π_name(σ_score>=60(students))
```

Read it from inside out: first retain rows with score at least 60, then return their names.

```sql
SELECT DISTINCT name
FROM students
WHERE score >= 60;
```

Without `DISTINCT`, SQL may return the same name more than once. Distinct names are not the same as distinct people: two students can share a name. Include student IDs when identities must remain distinguishable.

Relational algebra describes the logical result. A database optimiser may choose a different physical execution order while preserving query semantics.

## 4. Joins: matched rows and preserved rows

An inner join combines matching rows and excludes unmatched rows. It does more than widen a table: it may remove unmatched inputs or multiply rows when several matches exist.

A left join preserves every left-side row, producing NULL right-side fields when no match exists.

For the lesson's hypothetical data:

| Student ID | Name | batch_id |
| --- | --- | ---: |
| 1 | Ali | 10 |
| 2 | Sara | 10 |
| 3 | Omar | 99 |

| Batch ID | Code |
| --- | --- |
| 10 | 23BSCYS |
| 20 | 22BSCYS |

The inner join returns Ali and Sara, each with 23BSCYS. The left join additionally returns Omar with NULL batch fields.

**Constraint clarification:** batch_id 99 with no matching batch cannot be inserted as a normal committed row under an active, enforced foreign key. Treat this as an unconstrained or dirty input example. The runnable demonstration uses a permitted NULL batch_id for Omar to illustrate the same unmatched-join behaviour.

## 5. Worked practice

### Practice 1 — Identify keys and relationships

Assuming the intended constraints are declared:

| Table | Primary key | Foreign keys |
| --- | --- | --- |
| students | id | batch_id → batches.id |
| batches | id | None in the supplied schema |
| courses | id | None in the supplied schema |
| enrolments | id | student_id → students.id; course_id → courses.id |

A batch can have many students. Students and courses form a many-to-many relationship through enrolments: one student can enrol in many courses, and one course can have many students.

Enrolments needs two foreign keys because each row must identify both participants in that relationship. Column names alone do not enforce these rules; explicit constraints do.

A unique pair `(student_id, course_id)` prevents repeated enrolment if the business rule allows only one per pair. Include term or offering information if re-enrolment is allowed.

### Practice 2 — Explain the anomalies

1. **Student changes name:** an update anomaly occurs when every enrolment copy must change and some copies may be missed.
2. **Course exists with no students:** an insertion anomaly occurs because the combined table offers no independent place for course facts.
3. **Last student drops a course:** a deletion anomaly occurs if deleting the enrolment also deletes the only record of the course.
4. **Rows disagree about a teacher:** redundant course facts have become inconsistent.

Use `students(id, name, batch_id)`, `batches(id, code)`, `courses(id, title, teacher)`, and `enrolments(id, student_id, course_id, grade)`. This assumes one teacher per course in the simplified example.

Store each fact according to its dependency so a single authoritative update replaces many coordinated edits.

### Practice 3 — Translate algebra and SQL

**1. Algebra to SQL**

```text
π_name(σ_score>=60(students))
```

```sql
SELECT DISTINCT name
FROM students
WHERE score >= 60;
```

This performs selection followed by projection.

**2. SQL to algebra**

```sql
SELECT id
FROM students
WHERE batch_id = 3;
```

```text
π_id(σ_batch_id=3(students))
```

This selects batch 3 rows and projects id. Since id is a primary key, duplicate elimination makes no difference here.

**3. Conditional join to SQL**

```text
students ⋈_(students.batch_id=batches.id) batches
```

```sql
SELECT students.*, batches.*
FROM students
JOIN batches ON students.batch_id = batches.id;
```

This is a conditional join, not an implicit natural join on every same-named column. Qualifying columns avoids confusing students.id with batches.id.

Recognising the operations lets us predict which rows and attributes a query can return.

### Practice 4 — Predict the join result

For the hypothetical tables in section 4:

| Join | Count | Students |
| --- | ---: | --- |
| INNER JOIN | 2 | Ali and Sara |
| LEFT JOIN with students on the left | 3 | Ali, Sara, and Omar |

Omar has no matching batch, so the inner join excludes him. The left join preserves him with NULL batch fields.

An inner join can silently undercount students when the reporting requirement includes students without a matched batch.

### Practice 5 — Design lesson-completion tracking

| Table | Columns and constraints |
| --- | --- |
| students | id primary key, name |
| courses | id primary key, title |
| lessons | id primary key, course_id NOT NULL foreign key to courses.id, title |
| completions | id primary key, student_id NOT NULL foreign key to students.id, lesson_id NOT NULL foreign key to lessons.id, completed_at NOT NULL |

Add `UNIQUE(student_id, lesson_id)` if each student can have only one completion record per lesson. If repeated attempts are required, model those explicitly instead.

- **Course → lessons:** one-to-many. Each lesson has exactly one valid course reference because course_id is a non-null foreign key. A course may have zero or more lessons.
- **Students ↔ lessons:** many-to-many through completions, whose two foreign keys identify a student and a lesson.

The course reference belongs in lessons for this one-course-per-lesson requirement. A separate course–lesson bridge would be appropriate if lessons could belong to multiple courses.

## 6. Runnable SQL demonstration

[examples.sql](./examples.sql) contains SQLite-compatible table definitions, sample records, and queries. Run it in a fresh database.

The extra students.score field is a teaching simplification for the algebra examples; per-course grades remain in enrolments. The lesson-title placeholder is sample data, not a published course lesson.

Expected results:

| Query | Result |
| --- | --- |
| Names with score ≥ 60 | Ali, Sara |
| Students INNER JOIN batches | Ali / 23BSCYS; Sara / 23BSCYS |
| Students LEFT JOIN batches | Above rows plus Omar / NULL |
| Names enrolled in course 101 | Ali, Sara |
| Student IDs in course 101 ∪ course 102 | 1, 2 |
| Student IDs in course 101 − course 102 | 2 |

The fixture enables SQLite foreign-key enforcement for its connection. Its completion design permits one completion per student–lesson pair.

## 7. Theory exercises — suggested answers

These are study references. Explain the concepts in your own words when submitting course work.

### Task 1 — Database key definitions

A primary key uniquely identifies each row within a table and cannot contain NULL. It can consist of one column or several columns.

A foreign key references an eligible key in another table, or in the same table. When enforced, it ensures that non-null references match existing records.

Together, they let tables represent connected facts. For example, students.id identifies a student, and enrolments.student_id connects an enrolment to that student without repeating all the student's details.

### Task 2 — The purpose of normalisation

Normalisation organises data into related tables to reduce unnecessary repetition and avoid anomalies. In a large denormalised table, a student name might appear once for every enrolment. A name change would then require many updates. Missing one update leaves conflicting names for the same student.

Keeping student details in students and referencing the student from enrolments allows the name to be updated in one authoritative record.

### Task 3 — Relational-algebra mapping

| SQL component | Operation | What it returns |
| --- | --- | --- |
| WHERE | Selection, σ | Rows satisfying the specified condition |
| SELECT column list | Projection, π | The chosen attributes |
| JOIN ... ON | Join, ⋈ | Combined rows satisfying the join predicate |

Classical projection removes duplicate tuples; SQL needs DISTINCT when that set behaviour is required. An inner join includes matches only, while a left join also preserves unmatched left rows.

### Task 4 — Union versus difference

Union, A ∪ B, returns all distinct rows appearing in A, B, or both.

Difference, A − B, returns only rows present in A and absent from B. The order matters: reversing the operands can change the result.

Both operations require compatible relation schemas. For example, if A contains student IDs {1, 2} and B contains {1}, their union is {1, 2}, while A − B is {2}.

### Task 5 — Decompose a query

To find the names of students enrolled in a specific course:

1. **Selection:** retain enrolments whose course_id matches the required course.
2. **Join:** connect those enrolments to students using enrolments.student_id = students.id.
3. **Projection:** keep the student name attribute.

If the course is specified by title rather than ID, join courses and select the intended course there. IDs avoid ambiguity when course titles repeat.

```sql
SELECT DISTINCT s.name
FROM students AS s
JOIN enrolments AS e ON e.student_id = s.id
WHERE e.course_id = 101;
```

This returns distinct names, so different students sharing a name will collapse to one output value. Include s.id alongside s.name when the result should identify individual students.

## 8. Quick revision

- A primary key identifies; a foreign key connects and enforces valid references.
- Normalisation reduces redundancy and update, insertion, and deletion anomalies.
- σ selects rows; π projects attributes; ⋈ joins matching tuples.
- Union includes either relation; difference keeps the first relation's unmatched tuples.
- SQL has duplicate-preserving behaviour unless elimination is requested.
- No row order is guaranteed without ORDER BY.
- Inner joins can lose unmatched records; left joins preserve the left side.
- NOT NULL, FOREIGN KEY, and UNIQUE enforce different parts of a relationship.

## Sources

- User-supplied course material: *Data Science and Analytics, Module IV: Review of Relational Algebra and SQL, Relational Databases and Relational Algebra*.
- [PostgreSQL: Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) — key and reference semantics.
- [PostgreSQL: Select Lists](https://www.postgresql.org/docs/current/queries-select-lists.html) — projection and duplicate elimination in SQL.
- [PostgreSQL: Combining Queries](https://www.postgresql.org/docs/current/queries-union.html) — set operations and compatible inputs.

Worked responses and clarifying notes were prepared for this repository.

[Module overview](./README.md) · [Theory index](../README.md)
