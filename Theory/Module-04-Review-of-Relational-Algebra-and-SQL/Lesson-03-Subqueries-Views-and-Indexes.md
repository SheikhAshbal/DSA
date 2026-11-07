# Lesson 3: Subqueries, Views and Indexes

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-02-SQL-Basics.md)

**Course:** Data Science and Analytics  
**Module IV:** Review of Relational Algebra and SQL  
**Estimated study time:** 50 minutes

## Learning objectives

- Use a subquery to express a comparison with another query result.
- Create and reuse an ordinary SQL view.
- Explain the read, write, and storage trade-offs of indexes.
- Inspect an SQLite query plan.
- Design an above-batch-average report with a stated averaging rule.

## 1. Subqueries: an intermediate question

A subquery is a query nested within another SQL statement. It can provide a scalar value, a set of values, or a derived table.

For an above-overall-average question, the scalar subquery supplies the comparison value:

```sql
SELECT s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score > (SELECT AVG(score) FROM enrolments)
ORDER BY e.score DESC, e.id ASC;
```

On the Lesson 2 fixture, the mean is:

```text
(88 + 72 + 91 + 55 + 63) / 5 = 73.8
```

The result contains Ali's Security score 91 and Data Science score 88.

Conceptually, calculate the benchmark and compare each outer row with it. The inner AVG ignores NULL scores; an outer NULL score does not satisfy the greater-than comparison.

### Logical dependency versus physical execution

The inner query here is **uncorrelated**: it does not reference an outer row. The optimiser decides how to execute it. Do not assume all subqueries run once, literally inside-out.

A **correlated** subquery references outer-query values and conceptually depends on each outer row or group. The engine may still optimise or transform its execution.

A scalar subquery is a clear solution for this exercise, but not the only one. A derived-table join or window-function approach can also express an above-average comparison. The important requirement is to compute the benchmark at the correct level; a current-query aggregate cannot simply be placed in a flat row-level WHERE.

The lesson's opening shorthand selected name directly from enrolments. Under the actual Lesson 2 schema, name lives in students, so the example above includes the required join.

## 2. Views: name and reuse a query

An ordinary view stores a query definition that can be used as a table-like source.

```sql
CREATE VIEW passing AS
SELECT e.id AS enrolment_id, s.id AS student_id,
       s.name, e.course, e.score
FROM enrolments AS e
JOIN students AS s ON e.student_id = s.id
WHERE e.score >= 60;
```

Keeping identifiers in the view preserves record identity and enables deterministic tie-breaking.

Later queries can read from passing without repeating its join and threshold:

```sql
SELECT course, COUNT(*) AS n_passing
FROM passing
GROUP BY course
ORDER BY course;
```

### View versus physical table

| Property | Ordinary view | Physical table |
| --- | --- | --- |
| What is stored | Query definition | Stored rows |
| Independent copy of result rows | No | Yes, if populated from a query |
| Response to base-table changes | Re-evaluates against data visible to the query | A separately copied result does not update itself |
| Main purpose here | Reuse and centralise logic | Store the underlying facts |

“Current” means data visible under the connection's transaction and isolation rules. An ongoing snapshot may not see another transaction's later commit immediately.

A materialised view or manually maintained summary table is different: it stores results and needs a refresh or maintenance policy. An ordinary view does not automatically cache or speed up its query, nor does it run a weekly report on a schedule.

Centralising logic makes maintenance easier, but changing a view is still a schema change that should be reviewed for its effects on dependent reports.

## 3. Indexes: targeted access at a cost

An index is an auxiliary lookup structure over selected values. Common SQLite indexes use ordered B-tree structures and can support equality searches, ranges, and suitable ordering.

| Potential read benefit | Associated cost |
| --- | --- |
| Locate selective matches without a full table scan | Extra storage and cache usage |
| Assist joins on indexed lookup keys | Work to maintain entries on inserts and deletes |
| Support range searches and some sort orders | Maintenance when indexed values change |
| Sometimes answer queries from index entries alone | Build time and operational complexity |

An index does not guarantee a faster plan. The planner may prefer a scan for a tiny table or when a query retrieves much of the table. An update to an unrelated column need not rewrite every index entry.

Do not interpret the lesson's binary-search illustration as a guarantee of 24 disk reads for ten million rows. B-tree fan-out, caching, matching-row count, and table lookups determine actual work. Finding a key and returning millions of matching rows are different costs.

### Inspect before claiming a speedup

```sql
CREATE INDEX IF NOT EXISTS idx_enrol_student
ON enrolments(student_id);
```

```sql
EXPLAIN QUERY PLAN
SELECT * FROM enrolments WHERE student_id = 1;
```

Look for a search using idx_enrol_student rather than assuming its exact output wording. A plan shows an access strategy, not elapsed time. Measure a representative workload before making performance claims. See [SQLite's query-plan guide](https://www.sqlite.org/eqp.html).

## 4. Runnable demonstration

[lesson03-queries.sql](./lesson03-queries.sql) reuses [lesson02-setup.sql](./lesson02-setup.sql). It creates two views and one index, then runs the lesson queries.

For a fresh database, run these commands from the directory containing the SQL files, with the SQLite CLI installed:

```powershell
Get-Content -Raw -LiteralPath './lesson02-setup.sql' | sqlite3 dsa-lesson03.db
Get-Content -Raw -LiteralPath './lesson03-queries.sql' | sqlite3 -header -column dsa-lesson03.db
```

If you already have the Lesson 2 practice database, run only lesson03-queries.sql against that database. Run the view definitions once; subsequent reports can query the views directly. The script does not drop or overwrite existing objects.

| Query | Expected result on the five-row fixture |
| --- | --- |
| Above overall average | Ali / Security / 91; Ali / Data Science / 88 |
| Passing counts | Data Science: 2; Security: 2 |
| Top two passing enrolments | Ali / Security / 91; Ali / Data Science / 88 |
| Equality lookup plan | Planner can use idx_enrol_student |
| Above own batch benchmark | Ali, 23BSCYS, student average 89.5, batch average 78.5 |

Exact query-plan text can vary by SQLite version.

## 5. Worked practice

### Practice 1 — Above the overall average

Use the scalar subquery in section 1. It produces 73.8 as the benchmark; the outer query keeps scores strictly greater than that value and joins to students to retrieve names.

This separates two questions: “What is the overall mean?” and “Which enrolments exceed it?”

### Practice 2 — Define and reuse passing

Create the passing view from section 2 and query it for course counts. It returns two passing enrolments in each course.

For the top two:

```sql
SELECT name, course, score
FROM passing
ORDER BY score DESC, enrolment_id ASC
LIMIT 2;
```

Both rows belong to Ali, with scores 91 and 88. These are enrolment records, not two distinct students.

The passing threshold and join live in one definition. Future queries use that definition against the base data visible at query time.

### Practice 3 — Create an index and inspect the plan

Create idx_enrol_student and run EXPLAIN QUERY PLAN as shown in section 3.

On a large table, selective student_id lookups can avoid examining every row. The index consumes storage and requires maintenance as enrolment records are inserted, deleted, or have their indexed key changed.

The tiny fixture demonstrates usage, not a production speed benchmark.

### Practice 4 — Choose columns for the login workload

| Column | Initial decision | Reason |
| --- | --- | --- |
| user_id | Strong index candidate | Frequent equality filters and joins |
| logged_at | Strong index candidate | Frequent time-range predicates |
| user_agent | Do not add a routine index for the stated workload | Rare queries offer little benefit; a normal B-tree often cannot accelerate a leading-wildcard pattern |
| ip | No new index without evidence | No frequent predicate is supplied |
| country | No new standalone index by default | No frequent use is supplied; few distinct values may make common-value lookups unselective |
| id | Inspect existing primary-key access first | Avoid an unnecessary duplicate index |

Low cardinality alone does not make an index useless: a rare country value could still be selective. Likewise, whether LIKE can use an index depends on its pattern and database settings.

If frequent queries filter by user_id and logged_at together, consider a composite (user_id, logged_at) index and inspect the plans. It is not automatically a replacement for logged_at-only access.

Indexing everything adds write and storage cost whether or not queries benefit.

### Practice 5 — Compose a weekly batch report

“Batch average” needs a precise definition. This implementation gives **each student with at least one known score equal weight**:

1. Calculate each student's mean across known scores.
2. Calculate each batch's mean of those student means.
3. Join student means to their batch benchmark.
4. Keep student means strictly above that benchmark.
5. Save the result as above_batch_students for reuse.

The SQL file implements this with named query expressions in a WITH clause:

```sql
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
```

WITH expressions name intermediate query results for this statement; they are not separately stored ordinary views.

On the fixture, Ali's mean is 89.5 and Sara's is 67.5, so their batch benchmark is 78.5. Omar's single-student batch has a benchmark of 55; his mean equals it, so he does not pass the strict comparison.

Students without known scores are excluded from both the comparison and benchmark. A batch average across all enrolment scores is another valid definition, but gives students with more attempts more weight and can produce different results.

The existing enrolments(student_id) index is a candidate for relevant joins. A students(batch) index should be justified by actual plans and workload; an all-batch aggregation can still need to read most records.

**Division of labour:** intermediate queries calculate comparisons, the view names the reusable report, and suitable indexes may reduce access costs. A scheduler is needed separately if the report must run automatically each week.

## 6. Theory exercises — suggested answers

Use these as study references and explain the concepts in your own words for course submissions.

### Task 1 — Subquery logic and execution

An above-average filter needs a benchmark calculated from multiple records before individual scores can be compared with it. A scalar subquery can calculate AVG(score), and the outer query can keep rows whose scores exceed that result.

Conceptually, the inner result supplies the value used by the outer comparison. In this uncorrelated example, the average is independent of each outer row. The optimiser controls physical execution, so this is not a universal promise that all subqueries run once in a fixed order. Other SQL constructions can also express the same comparison.

### Task 2 — The nature of views

A physical table stores rows. An ordinary view stores a query definition, not an independent copy of the rows returned by that query.

Selecting from the view uses the underlying data visible to the current query or transaction, so there is no separate copied result to refresh. A materialised view is different because it stores results and needs a refresh or maintenance policy.

### Task 3 — Index trade-offs

An index can make selective filters, joins, and range searches faster by providing an access path that avoids a full table scan. Some indexes can also assist sorting or cover all the columns a query needs.

The trade-off is extra disk and memory pressure, creation cost, and maintenance during inserts, deletes, and changes to indexed values. Indexes should therefore serve real query patterns rather than be added to every column.

### Task 4 — Indexing strategy application

Column A is a strong index candidate because frequent filters on a ten-million-row table may otherwise require expensive scans. Check predicate types, selectivity, and execution plans to confirm the benefit.

Column B is not a good default candidate under the stated workload. It rarely helps filtering, while frequent changes to its indexed values would require repeated index maintenance. Leave it unindexed unless another important query or constraint provides a reason.

### Task 5 — View use-case analysis

Suppose several weekly reports need passing students' names, courses, and scores. Each would otherwise repeat the same join and passing-score filter.

A passing view defines that logic once. Reports can query the view directly, making them shorter and easier to maintain. If the rule changes, the definition can be changed centrally and dependent reports checked, rather than editing many separate copies. An ordinary view queries visible base data rather than maintaining a separate result snapshot.

## 7. Module revision checklist

- [ ] Identify primary keys, foreign keys, and the intended observational unit.
- [ ] Reduce redundancy and understand update, insertion, and deletion anomalies.
- [ ] Distinguish selection, projection, joins, and set operations.
- [ ] Filter rows with WHERE and groups with HAVING.
- [ ] Use logical query order without assuming a fixed physical plan.
- [ ] State the population and weighting used in every average.
- [ ] Use views for reusable definitions, not automatic caching or scheduling.
- [ ] Choose indexes for measured access patterns and inspect their plans.
- [ ] Keep deterministic ordering when ranking results.

## Sources

- User-supplied course material: *Data Science and Analytics, Module IV: Review of Relational Algebra and SQL, Subqueries, Views and Indexes*.
- [SQLite: CREATE VIEW](https://www.sqlite.org/lang_createview.html) — named query definitions.
- [SQLite: Query Planning](https://www.sqlite.org/queryplanner.html) — index access and query-plan selection.
- [SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) — interpreting scans, searches, and index usage.

Worked responses and clarifying notes were prepared for this repository.

[Previous lesson](./Lesson-02-SQL-Basics.md) · [Module overview](./README.md) · [Theory index](../README.md)
