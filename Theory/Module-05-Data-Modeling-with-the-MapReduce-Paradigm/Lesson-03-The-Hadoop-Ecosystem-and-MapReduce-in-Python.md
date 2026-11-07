# Lesson 3: The Hadoop Ecosystem and MapReduce in Python

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-02-The-MapReduce-Model.md)

**Course:** Data Science and Analytics  
**Module V:** Data Modeling with the MapReduce Paradigm  
**Estimated study time:** 50 minutes

## Learning objectives

- Distinguish HDFS storage, YARN resource management, and MapReduce processing.
- Explain data locality and its limits.
- Place Hive, Pig, HBase, and Spark in the ecosystem.
- Write Python programs using the Hadoop Streaming text protocol.
- Run and adapt a local map–sort–reduce pipeline.

## 1. Hadoop's storage, resource, and processing roles

The three components emphasised in this lesson are:

| Component | Main responsibility |
| --- | --- |
| HDFS — Hadoop Distributed File System | Store files across DataNodes as blocks, commonly with replication |
| YARN — Yet Another Resource Negotiator | Allocate cluster resources and support application scheduling |
| MapReduce | Execute distributed map/reduce computations |

Hadoop also includes common libraries and utilities. The three items above are the lesson's storage–resources–processing model, not an exhaustive list of every Hadoop module.

HDFS metadata identifies files and their block locations. DataNodes store blocks. Replication supports recovery from a DataNode loss when surviving replicas remain available; it is not an unconditional guarantee against every failure or accidental deletion.

In YARN, resource allocation and application task management are divided among components. The ResourceManager allocates resources, NodeManagers manage worker containers, and an application's ApplicationMaster negotiates resources and coordinates its tasks.

Separating the roles allows different processing engines to use the storage and resource layers. It does not mean that capacity planning is completely independent when compute and storage share physical nodes.

## 2. Data locality: bring computation near input

Data locality means scheduling work near the data it needs, preferably on a node holding the input block or otherwise nearby in the network.

Moving a small program or launching a task near a large input can avoid shipping the whole input to a central processor. This matters when input volumes are very large.

Locality is an optimisation goal, not an absolute rule. A node may have insufficient resources, tasks may need remote input, and shuffle transfers intermediate data between workers. Program startup, dependencies, replication, and output also have costs.

The course's petabyte-versus-kilobytes comparison illustrates the difference in scale. It does not imply that all network movement disappears or that shipping code takes no time. See the [HDFS architecture reference](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html).

## 3. Tools around Hadoop

| Tool | Course role | Typical need illustrated |
| --- | --- | --- |
| Hive | SQL-oriented analytics over distributed data | Query large datasets without hand-writing mapper/reducer programs |
| Pig | Data-flow scripting, associated with Pig Latin | Express a sequence of transformations as a pipeline |
| HBase | Distributed database supporting key-based reads and writes | Retrieve or update individual records in a large table |
| Spark | General distributed processing with reusable intermediate data | Iterative or interactive workloads |

These tools are not simply interchangeable layers of one MapReduce job.

Historically, Hive translated SQL-style queries into MapReduce work. Avoid assuming every Hive deployment today executes through raw MapReduce; its interface and execution backend are separate concerns.

Spark is a processing engine rather than a wrapper that necessarily generates Hadoop MapReduce jobs. It can use Hadoop storage and cluster infrastructure and can cache reusable data. Memory, network, spills, and the algorithm still determine performance: it is not always faster for every workload.

Pig is included to explain the ecosystem described in the course, rather than to make a blanket recommendation for new projects.

## 4. Hadoop Streaming: stdin and stdout as the interface

Hadoop Streaming lets external programs implement map and reduce operations through standard input and standard output.

For this word-count example:

| Stage | Input | Output |
| --- | --- | --- |
| Mapper | Lines of source text | One word TAB 1 per token |
| Framework shuffle | Intermediate key/value records | Same-key records routed and grouped for reducers |
| Reducer | Consecutive key TAB integer-count records | One key TAB total for each group |

The default Streaming convention uses the first tab to separate key from value in mapper output. Input and output formats can be configured, so the token-count example is not the only supported protocol.

Keep stdout for result records. Write diagnostics to stderr so logs do not become malformed key/value input.

### Mapper

[mapper.py](./lesson03-python/mapper.py) splits each line on whitespace and emits a count:

```python
for line in sys.stdin:
    for word in line.split():
        print(f"{word}\t1")
```

### Reducer

[reducer.py](./lesson03-python/reducer.py) keeps a current key and total. It adds counts while the key stays the same, emits the previous total when the key changes, and emits the final total at end-of-file.

Without grouped input, the same key could appear in several separated runs and produce several partial output rows instead of one global count. The included reducer rejects decreasing keys to catch unsorted local input.

Its memory use is constant with respect to the number of keys: it stores the current key and running total rather than all groups. It accepts nonnegative integer counts and reports malformed records as errors.

## 5. Local files and execution

The [lesson03-python](./lesson03-python/README.md) example directory contains:

| File | Purpose |
| --- | --- |
| [docs.txt](./lesson03-python/docs.txt) | Two sample lines |
| [mapper.py](./lesson03-python/mapper.py) | Count each word |
| [initial_mapper.py](./lesson03-python/initial_mapper.py) | Count each starting character |
| [reducer.py](./lesson03-python/reducer.py) | Sum grouped counts |
| [run_local.py](./lesson03-python/run_local.py) | Execute the scripts with a small in-memory sort |

All examples preserve case and punctuation. “Starting letter” means the first character of each whitespace-delimited token in this exercise. Real text may need explicit case, punctuation, and Unicode policies.

### Windows-friendly runner

From the example directory, using Python 3:

```powershell
python run_local.py docs.txt
python run_local.py docs.txt --initial-letter
```

The runner invokes the actual mapper and reducer as subprocesses using the same Python interpreter. It sorts intermediate records in memory for this tiny dataset. It is not an external-memory sorter or a distributed runtime.

### Unix pipeline

With Python 3 and a Unix sort executable:

```bash
cat docs.txt | python3 mapper.py | LC_ALL=C sort | python3 reducer.py
cat docs.txt | python3 initial_mapper.py | LC_ALL=C sort | python3 reducer.py
```

LC_ALL=C makes the sorting convention explicit. The mapper's keys have no tabs or whitespace because tokens are split on whitespace.

In this local illustration, sort groups identical keys. A real Hadoop shuffle additionally partitions, transfers, and merges records from many map tasks. The Unix pipeline does not simulate network traffic, scheduler behaviour, retries, or HDFS.

Do not assume PowerShell's sort alias is the Unix sort executable. Use the Python runner on Windows when no Unix toolchain is installed.

## 6. Worked practice

### Practice 1 — Assign component responsibilities

1. Splitting and storing a 10 TB file in replicated blocks: **HDFS**.
2. Allocating CPU and memory to applications: **YARN**, working with application-level task management.
3. Executing map and reduce computations: **MapReduce**.
4. Preserving access after a DataNode loss: **HDFS replication**, subject to surviving replicas and overall availability.

Data locality tries to place map tasks near the blocks they read instead of gathering all input onto one central machine. The separate layers can evolve and be managed for their own responsibilities, while still sharing physical resource limits.

### Practice 2 — Match ecosystem tools to needs

| Need | Course answer | Reason |
| --- | --- | --- |
| SQL-based analysis of a petabyte | Hive | SQL interface over distributed data |
| Fifty iterations over reusable data | Spark | Can reuse cached intermediate data rather than repeating all reads |
| Low-latency key-based record reads and writes | HBase | Database access rather than a batch scan |
| Scripted multi-step data flow | Pig | Data-flow language |

Hive's advantage in this comparison is its SQL interface. Spark's advantage for iteration is its execution and data-reuse model. These are different dimensions, and Spark also offers SQL.

The workload and deployment determine the actual engine and performance; avoid treating either tool as a universal replacement for every other component.

### Practice 3 — Write the Python programs

The mapper emits one tab-delimited pair per word. The reducer parses key and count, accumulates consecutive equal keys, flushes when the key changes, and flushes once more at EOF.

The full scripts are linked in section 5. They use only the Python standard library.

Sorted grouping is essential because this reducer processes one group at a time. It has no dictionary of previously completed keys.

### Practice 4 — Run the word-count pipeline

Input:

```text
data is data
data science is fun
```

Expected output, with a tab between fields:

```text
data	3
fun	1
is	2
science	1
```

There are seven tokens in total: 3 + 1 + 2 + 1 = 7. The sort stage brings the three data contributions and two is contributions together.

The program logic is compatible with Hadoop Streaming's interface. Running it on a cluster still requires distributing the scripts, providing a suitable Python runtime on workers, configuring input/output paths, and submitting the job. A local run alone does not verify those deployment steps.

### Practice 5 — Change only the mapper's key

[initial_mapper.py](./lesson03-python/initial_mapper.py) changes the emission to:

```python
print(f"{word[0]}\t1")
```

Using the same reducer gives:

```text
d	3
f	1
i	2
s	1
```

The map key changed from a whole word to its first character. Grouping and summation were reused unchanged.

The awkward sentence in the course prompt about average word length is not a limitation of MapReduce: a mean can be computed with (sum_of_lengths, count), as explained in Lesson 2. This exercise deliberately uses counting to reuse the existing integer-sum reducer.

## 7. Theory exercises — suggested answers

These are study references. Explain the concepts in your own words when submitting course work.

### Task 1 — Core Hadoop components

- **HDFS** stores large files as blocks distributed across storage nodes, commonly replicated to support recovery from node failures.
- **YARN** manages cluster resources and supports application scheduling, including CPU and memory allocation.
- **MapReduce** is the processing framework that executes map and reduce tasks over partitioned data.

These are the three roles emphasised in the lesson: storage, resource management, and processing.

### Task 2 — Data locality reasoning

Data locality means placing computation on or near a machine holding the required input. Instead of transferring a huge dataset to a central processor, the system tries to launch relatively small task code near the data blocks.

For petabyte-scale input, avoiding unnecessary bulk network transfer can save substantial time and bandwidth. Locality does not eliminate all communication: shuffle and other remote operations still move data.

### Task 3 — Comparing Spark and Hive

Hive provides a SQL-oriented way to analyse distributed data, so analysts can express queries without writing map and reduce functions. Historically, Hive compiled such queries into MapReduce jobs; the execution backend depends on the deployment.

Spark is a separate distributed processing engine. Its ability to reuse cached datasets can reduce repeated I/O in iterative workloads that fit classic MapReduce poorly. Hive's interface advantage and Spark's execution advantage are related to different parts of the problem; Spark can also be used through SQL.

### Task 4 — The role of shuffle

In the local pipeline, sort puts records with the same key next to one another. The reducer can then add a group's values and finish that group when the key changes.

This represents the grouping and ordering aspect of shuffle. In distributed MapReduce, the framework also routes and transfers intermediate records from different map tasks to the responsible reducers.

### Task 5 — Python MapReduce logic

In this word-count example, the mapper reads source-text lines from stdin and writes one word TAB 1 record per token to stdout.

The reducer receives grouped key TAB integer-count lines through stdin. It parses each line and adds the count to the current key's total. When a new key appears, it emits the completed key and total, resets its accumulator, and starts the next group. At EOF, it emits the final group.

The reducer outputs key TAB total lines. Hadoop Streaming can configure other formats, but the first-tab convention is the default used here.

## 8. Module revision checklist

- [ ] Explain when volume or velocity justifies distribution.
- [ ] Distinguish scaling up from scaling out.
- [ ] Identify map output, shuffle groups, and reducer results.
- [ ] Choose correct keys and safe partial aggregation states.
- [ ] Distinguish HDFS, YARN, and MapReduce.
- [ ] Explain data locality without assuming zero network movement.
- [ ] Place ecosystem tools by their roles rather than treating them as interchangeable.
- [ ] Keep Streaming stdout clean and group input before reduction.
- [ ] Separate a local demonstration from an actual cluster deployment.

## Sources

- User-supplied course material: *Module V: Data Modeling with the MapReduce Paradigm, The Hadoop Ecosystem and MapReduce in Python*.
- [Apache Hadoop: HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html).
- [Apache Hadoop: YARN](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html).
- [Apache Hadoop: Streaming](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html).
- [Apache Hive](https://hive.apache.org/) — SQL-oriented distributed analytics.
- [Apache Spark: RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html) — data reuse and persistence.

Worked responses, clarifying notes, and the local Python examples were prepared for this repository.

[Previous lesson](./Lesson-02-The-MapReduce-Model.md) · [Module overview](./README.md) · [Theory index](../README.md)
