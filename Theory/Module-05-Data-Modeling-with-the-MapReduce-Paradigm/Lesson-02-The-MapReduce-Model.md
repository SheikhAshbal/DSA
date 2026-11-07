# Lesson 2: The MapReduce Model — Map, Shuffle, Reduce

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-01-Big-Data-and-Distributed-Computing.md)

**Course:** Data Science and Analytics  
**Module V:** Data Modeling with the MapReduce Paradigm  
**Estimated study time:** 55 minutes

## Learning objectives

- Describe the three phases and their key–value data shapes.
- Choose keys that express the required grouping.
- Trace word count by hand.
- Design a failed-login counting job.
- Explain shuffle costs and safe local aggregation.
- Recognise workloads that fit classic MapReduce poorly.

## 1. The three-phase model

| Phase | Who supplies the logic? | Conceptual input → output | Purpose |
| --- | --- | --- | --- |
| Map | Developer | One input record → zero or more intermediate (key, value) pairs | Transform, filter, or emit information independently |
| Shuffle and grouping | Framework | Intermediate pairs → each key with its associated values | Route and group records for reduction |
| Reduce | Developer | One key and its values → zero or more output pairs | Compute the group's result |

The course describes reducer values as a list. Production APIs often provide an iterator, so a reducer need not load an entire group into memory.

Map functions can process records without coordinating with other map calls. Reduction is independent across keys, although one reducer task can handle many keys. The scheduler determines where and when tasks run; not every node necessarily runs a mapper simultaneously.

The developer normally does not implement the shuffle transport, but can configure partitions and other policies. Framework support does not remove the need to choose correct keys.

```text
Input records
    |
    v
MAP: emit (key, value)
    |
    v
SHUFFLE: route and group equal keys
    |
    v
REDUCE: aggregate each key's values
    |
    v
Output pairs
```

## 2. Word count: follow the data shape

For each word, emit its text as the key and integer 1 as the value.

### Two mapper inputs

```text
Mapper A: "data is data"
Mapper B: "data science"
```

### Map output

```text
A -> ("data", 1), ("is", 1), ("data", 1)
B -> ("data", 1), ("science", 1)
```

### Shuffle output

```text
"data"    -> [1, 1, 1]
"is"      -> [1]
"science" -> [1]
```

### Reduce output

```text
("data", 3)
("is", 1)
("science", 1)
```

The count of data is 3, matching a direct count of the original text. Key order and value order are not important for this sum.

Define tokenisation before counting. These examples split on whitespace and preserve case and punctuation. A real task must specify whether Data, data, and data! are the same token.

## 3. Choosing a key is choosing a grouping

The map key plays the role of a SQL GROUP BY expression.

| Question | Map key | Map value | Reduce operation |
| --- | --- | --- | --- |
| Average score per batch | batch | score, or (score, 1) for partial aggregation | Sum and count, then divide |
| Enrolments per course | course | 1 | Sum |
| Highest score per student | student ID | score | Maximum |
| Total number of records | One constant key | 1 | Sum |
| Passing enrolments per course | course, only when score meets the threshold | 1 | Sum |

A constant key creates a global group and can concentrate work on one reducer. Partial aggregation or multiple stages can reduce the bottleneck.

Use stable student identifiers when names are not unique. Decide how to handle missing or invalid scores before mapping them.

### Safe averaging with partial aggregates

Averages cannot be combined by simply averaging mapper averages when their counts differ.

```text
Partition A: [0]             -> mean 0, count 1
Partition B: [100,100,100]   -> mean 100, count 3

Mean of the two means: (0 + 100) / 2 = 50   <- wrong
Overall mean: (0 + 300) / (1 + 3) = 75      <- correct
```

Emit (score, 1), merge pairs by adding their sums and counts, and divide only at the final reduction. The intermediate representation preserves the information needed for correct weighting.

## 4. Associativity, order, and combiners

Associativity means regrouping an operation does not change its result:

```text
(a + b) + c = a + (b + c)
```

Commutativity means changing the order does not change its result. Integer addition has both properties, so partial word counts can be grouped and combined in different orders.

These properties make sum a safe combiner operation. A **combiner** performs optional local aggregation before records are shuffled, reducing intermediate traffic when repeated keys occur locally.

A framework can skip a combiner or apply it multiple times. Correctness must not depend on exactly one combiner call. Its outputs must remain valid inputs for later combination and final reduction. See the [Hadoop MapReduce tutorial](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html).

Not every reducer is a valid combiner: returning a final average discards its count. Use a mergeable (sum, count) state instead.

Associativity is not a requirement that every possible reducer be a simple associative operation. It is the key property when arbitrary partial aggregation is used. Floating-point addition can also vary slightly with evaluation order, unlike the small exact integer counts used here.

## 5. What fits the model?

| Workload | Fit | Reason |
| --- | --- | --- |
| Count error codes in a very large log archive | Good | Records map independently and counts combine |
| Filter records by a local condition | Good | Each record can be accepted or rejected independently |
| Aggregate totals or maxima per key | Good | Groups can be reduced independently |
| A genuinely sequential recurrence | Poor | Each step needs a prior result |
| Repeated full-data passes for iterative training | Often poor for classic MapReduce | Repeated job setup, materialisation, and I/O add overhead |

Filtering can be a map-only job; a reducer is not required when no grouping or aggregation is needed.

A running total is not inherently impossible to parallelise. Associative prefix sums have parallel algorithms, but an ordered cumulative result is not a simple independent per-key reduction and may require extra stages.

Classic Hadoop MapReduce can spill and materialise intermediate data and write results between jobs. It is too broad to say every phase always writes every result to disk. Engines such as Spark support reusable cached datasets that can help iterative workloads, subject to memory and persistence choices. See [Spark's RDD guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html).

## 6. Shuffle costs

Values emitted on different mapper hosts must be brought to the reducer responsible for their key. This involves partitioning, serialisation, transfer, sorting or merging, and often local disk activity.

Three useful distinctions:

- **Total emitted bytes:** more or larger intermediate records usually increase movement and processing.
- **Distinct keys:** influence grouping and metadata costs, but do not alone determine the number of pairs or bytes.
- **Skew:** one very common key can overload a reducer even if there are few distinct keys.

A million distinct keys does not necessarily mean more records than a million copies of one key. Likewise, a combiner helps when local repeated keys permit compression of partial results; it may do little when every local key is unique.

Some shuffle data can remain local. The goal is to reduce unnecessary transfers and work, not to assume every byte always crosses the network.

## 7. Worked practice

### Practice 1 — Trace two mappers

Use the trace in section 2:

1. A emits three pairs; B emits two.
2. Shuffle groups data with three 1s, is with one, and science with one.
3. Reduce outputs data=3, is=1, science=1.
4. The five total words match the sum of the output counts.

The mappers can work independently because each occurrence contributes its own count, and integer addition combines those contributions consistently.

### Practice 2 — Design the key and value

1. **Average per batch:** key=batch; value=score; reducer totals known scores and divides by their count. Use (sum, count) states when combining.
2. **Enrolments per course:** key=course; value=1; reducer sums the values.
3. **Highest score per student:** key=student ID; value=score; reducer takes the maximum.
4. **Global record count:** key=a fixed constant; value=1; reducer sums all contributions.

Each map key identifies the equivalent SQL GROUP BY grouping. A composite key represents grouping by several fields.

### Practice 3 — Judge suitability

- Error-code counting fits well because independent emissions can be summed per code.
- A strictly sequential recurrence fits poorly because one step cannot be evaluated without the previous state.
- Record filtering fits well and can be map-only.
- A model requiring 100 full passes can run through repeated jobs, but classic MapReduce often incurs costly repeated I/O and scheduling.

Reusable cached data and a more flexible execution model can make an alternative engine more suitable for iteration; that is a workload decision rather than a claim that all machine learning is incompatible with MapReduce.

### Practice 4 — Explain the shuffle bottleneck

1. Matching keys can originate on many hosts, so the framework routes their values to the responsible reducer.
2. This embodies the previous lesson's data-movement challenge, alongside partitioning and coordination.
3. Large intermediate volume, numerous groups, or skew can make shuffle the bottleneck.
4. A sum combiner can send one partial count per local key instead of many individual 1s.

For the word-count input, A can replace two data pairs with (data, 2). Total shuffled pairs decrease from five to four. Reduction still produces data=3.

### Practice 5 — Failed logins per user per day

**Input record:** one validated login event containing an event identifier, stable user identifier, timestamp, and status.

**Map:** derive the day using an agreed timezone. For a failed login, emit:

```text
((user_id, day), 1)
```

Emit nothing for successful logins.

**Shuffle:** group all contributions for the same user–day pair.

**Reduce:** sum the contributions and emit ((user_id, day), failed_count).

**Combiner:** sum local contributions using the same composite key.

The composite key makes both user and day part of the grouping. Using only a username would combine different days; using only a day would combine different users.

Define how accidental duplicate events and invalid timestamps are handled upstream. This design counts supplied events; it does not automatically detect source duplicates.

Groups with zero failures do not appear. Reporting explicit zero rows requires a separate set of expected user–day combinations.

## 8. Runnable local simulation

[lesson02-mapreduce-demo.mjs](./lesson02-mapreduce-demo.mjs) demonstrates grouping, optional local combination, and reduction using Node.js without third-party packages.

Run from the file's directory:

```powershell
node ./lesson02-mapreduce-demo.mjs
```

Expected output:

```text
word count: [["data",3],["is",1],["science",1]]
word pairs: 5 without combiner -> 4 with combiner
failed logins: [[["ali","2026-11-07"],3],[["sara","2026-11-07"],1],[["ali","2026-11-08"],1]]
batch means: [["A",75]]
```

This is a small single-process teaching simulation. Its input partitions are arrays; it models no network, actual concurrent workers, fault recovery, or performance at scale. Group values are materialised in memory, and output follows local insertion order rather than a distributed ordering guarantee.

The simulator supports string keys and arrays of strings, encoded consistently for the examples. Days are prevalidated. Counts and sums remain within JavaScript's exact integer range for these small fixtures.

## 9. Theory exercises — suggested answers

These are study references. Explain the ideas in your own words for course submissions.

### Task 1 — The three phases

**Map:** the developer writes a function that transforms one record into zero or more intermediate key–value pairs. Independent calls make parallel processing possible.

**Shuffle:** the framework routes and groups values with the same key, so each group can be processed together.

**Reduce:** the developer writes the per-key aggregation logic. It receives a key and its grouped values and emits the final result, such as a count or maximum.

### Task 2 — Word-count data shapes

For input data science data, map emits:

```text
("data", 1), ("science", 1), ("data", 1)
```

Shuffle groups the data key as:

```text
"data" -> [1, 1]
```

Reduce sums its values and outputs:

```text
("data", 2)
```

The science key separately produces ("science", 1).

### Task 3 — Keys for average scores

The map key should be the classroom batch, and the value should be the student's valid score. Shuffle brings scores for the same batch together. The reducer calculates their sum and divides by their count.

If local combiners are used, emit (score, 1) and combine sums and counts, then divide at the end. Averaging local averages would be wrong when partitions have different numbers of scores.

This computes a mean per supplied score record. If students have different numbers of tests and should receive equal weight, calculate student-level means first under an explicit policy.

### Task 4 — Suitability of MapReduce

Counting is a natural fit because each record contributes independently and partial counts can be combined per key.

An iterative learning algorithm repeatedly uses the dataset and updated state. Implementing this through many classic MapReduce jobs can require repeated setup, reading, and writing of materialised results. That overhead makes it less suitable than an execution model that can reuse intermediate data efficiently. The algorithm is not necessarily impossible in MapReduce; it is often inefficient.

### Task 5 — Associativity and parallel computation

Associativity means changing how additions are grouped does not change the total. Mappers can therefore produce separate partial counts and reducers can combine them to obtain the same count as one machine.

For example, two data occurrences on one mapper and one on another give 2 + 1 = 3, just like adding three individual 1s. Integer addition is also commutative, so reordering those contributions does not affect the answer.

Every occurrence must still be accounted for correctly; associativity alone does not fix lost input, duplicated source events, or an incorrect job implementation.

## 10. Quick revision

- Map emits; shuffle groups and routes; reduce aggregates.
- Keys define groups, including composite groups.
- Filtering can emit zero pairs.
- Integer sum supports safe partial counting.
- Merge (sum, count) to compute averages correctly.
- A combiner is optional and must preserve correctness.
- Shuffle cost depends on bytes, groups, and skew.
- Ordered dependencies and repeated full-data iteration need careful workload choices.

## Sources

- User-supplied course material: *Data Science and Analytics, Module V: Data Modeling with the MapReduce Paradigm, The MapReduce Model: Map, Shuffle, Reduce*.
- [Apache Hadoop: MapReduce Tutorial](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html) — framework stages and local combination.
- [Apache Spark: RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html) — reusable datasets and persistence.

Worked responses, clarifying notes, and the local simulation were prepared for this repository.

[Previous lesson](./Lesson-01-Big-Data-and-Distributed-Computing.md) · [Module overview](./README.md) · [Theory index](../README.md)
