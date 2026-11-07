# Module V: Data Modeling with the MapReduce Paradigm

[Back to Theory](../README.md)

This module covers distributed-computing trade-offs, the MapReduce model, and the Hadoop ecosystem. All three lessons are documented below.

## Lessons

| Lesson | Topic | Repository material |
| --- | --- | --- |
| 1 | [Big Data and Distributed Computing](./Lesson-01-Big-Data-and-Distributed-Computing.md) | Notes, five worked practice steps, and five suggested theory answers |
| 2 | [The MapReduce Model: Map, Shuffle, Reduce](./Lesson-02-The-MapReduce-Model.md) | Notes, five worked practice steps, five suggested theory answers, and a local simulation |
| 3 | [The Hadoop Ecosystem and MapReduce in Python](./Lesson-03-The-Hadoop-Ecosystem-and-MapReduce-in-Python.md) | Notes, five worked practice steps, five suggested theory answers, and Python examples |

## Learning objectives

- Characterise workloads through volume, velocity, and variety.
- Explain the limits of vertical scaling.
- Weigh horizontal scaling against coordination and operating costs.
- Recognise when efficient single-machine processing is sufficient.
- Identify the distributed execution responsibilities abstracted by MapReduce.
- Trace map, shuffle, and reduce data shapes.
- Choose keys and safe partial aggregations.
- Explain shuffle costs and suitable workloads.
- Distinguish Hadoop storage, resource management, and processing.
- Run Python mapper/reducer programs through a local grouped pipeline.

Lesson 1 is conceptual; its examples are architectural decisions rather than a deployed cluster or runtime benchmark.

## Local simulation

Run [lesson02-mapreduce-demo.mjs](./lesson02-mapreduce-demo.mjs) with Node.js for word count, failed-login counts, and safe batch averages. It is an in-memory teaching model, not a distributed runtime.

## Python pipeline

See [lesson03-python](./lesson03-python/README.md) for the word-count and starting-character pipelines, with a cross-platform local runner and Unix-pipe instructions in the lesson.

Repository availability describes documented material, not course grades or submission status.
