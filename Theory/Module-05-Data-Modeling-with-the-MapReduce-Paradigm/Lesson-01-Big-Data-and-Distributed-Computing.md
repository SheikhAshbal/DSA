# Lesson 1: Big Data and Distributed Computing

[Theory index](../README.md) · [Module overview](./README.md)

**Course:** Data Science and Analytics  
**Module V:** Data Modeling with the MapReduce Paradigm  
**Estimated study time:** 45 minutes

## Learning objectives

- Explain volume, velocity, and variety with concrete examples.
- Describe the physical, financial, and operational limits of vertical scaling.
- Explain horizontal scaling and its coordination costs.
- Identify workloads that justify distribution and those that do not.
- Describe the systems work a MapReduce framework abstracts.

## 1. What makes data “big”?

Big data describes workloads whose size, arrival rate, or complexity strain the available tools and resources. There is no universal byte threshold: the relevant question is whether the system can store and process the workload within its resource, time, and reliability requirements.

| V | Meaning | Main diagnostic question |
| --- | --- | --- |
| Volume | Amount of data to store and process | Can the available system hold and scan it within the required time? |
| Velocity | Rate of arrival and required response time | Can processing keep up without an unacceptable backlog? |
| Variety | Diversity of formats, structures, and meanings | Can the pipeline interpret and combine the sources correctly? |

A small dataset in many formats can be difficult without requiring a cluster. Variety creates an integration challenge; by itself, it does not prove that distribution is necessary.

A dataset larger than RAM also does not automatically require distribution. Chunked processing, databases, disk-based algorithms, better representations, or more capable single-machine tools may suffice.

### Size is not the only constraint

A workstation might store a dataset comfortably but take too long to process it for a required deadline. Conversely, a large file may be processed efficiently in chunks without being loaded all at once.

Measure peak working memory, CPU demand, I/O throughput, arrival rate, and completion time. File size alone is an incomplete capacity estimate.

## 2. Vertical scaling: make one machine larger

Vertical scaling, or scaling up, increases the capacity of one machine: more memory, faster or more processors, faster storage, or greater storage capacity.

It can preserve a simpler architecture and is often a sensible first response. However, it has limits:

1. **Hardware ceilings:** a platform supports only a finite amount of memory, processors, storage bandwidth, and expansion.
2. **Financial limits:** high-capacity hardware and upgrades may become poor value for the workload.
3. **Bottlenecks:** more RAM does not solve every CPU, disk, or software limitation.
4. **Operational risk:** if the workload relies on one unprotected host, that host's failure can interrupt the service or job.

A single machine can have backups and failover arrangements, so vertical scaling does not rule out resilience. The risk arises from relying on a single unprotected execution or storage location.

### Interpreting the lesson's cost illustration

The course compares one 512 GB server with 32 nodes containing 16 GB each:

```text
32 × 16 GB = 512 GB aggregate memory
```

The quoted costs are illustrative teaching figures, not current hardware quotations or a total-cost comparison.

Aggregate cluster RAM is not a single shared 512 GB address space. Each task must fit within its local resources, and some capacity is consumed by the operating system, framework, replication, and intermediate data. Network, power, administration, and software costs also affect the comparison.

## 3. Horizontal scaling: share the work across nodes

Horizontal scaling, or scaling out, adds machines and partitions work across them. A cluster can provide greater aggregate capacity and parallel throughput.

| Potential gain | Condition needed |
| --- | --- |
| Process larger datasets | Storage and computation must be partitionable |
| Improve throughput | Enough independent work exists to keep nodes busy |
| Expand incrementally | The architecture and workload support additional nodes |
| Recover from worker failure | Data durability, task retry, and recovery mechanisms are implemented |
| Improve cost effectiveness | Total operating cost is favourable for the workload |

Adding nodes does not provide limitless or perfectly linear speedup. Serial work, coordination, network traffic, skewed partitions, and shared bottlenecks can limit improvement.

### The four core distribution challenges

| Challenge | What must be solved | Example |
| --- | --- | --- |
| Partitioning | Divide data and tasks into useful, balanced pieces | A frequently occurring key overloads one worker |
| Coordination | Track dependencies and combine partial results correctly | Do not publish a report before all required partitions finish |
| Fault tolerance | Detect failures and recover without losing or incorrectly duplicating work | Re-run a failed task using durable input |
| Data movement | Transfer, serialise, and organise records across the network | Bring matching join keys together from different nodes |

Single-machine programs also partition work, coordinate threads, handle failures, and move data between memory and disk. Distribution makes these concerns harder because machines have separate memory, communication takes time, and one machine can fail while others continue.

### Why distributed joins can be expensive

If matching keys reside on different workers, rows may need to be redistributed so the matching data is processed together. This network redistribution is often called a shuffle.

Useful partitioning can reduce movement; a large join may still produce substantial intermediate data. Adding nodes does not remove the cost of transferring those records.

## 4. How MapReduce reduces the programming burden

MapReduce expresses suitable batch computations through map and reduce functions over key–value data. The framework handles much of the input partitioning, task scheduling, communication, and recovery machinery.

The programmer concentrates on domain logic:

```text
Input partitions
      |
      v
Map: produce intermediate key–value pairs
      |
      v
Framework: group and transfer values by key
      |
      v
Reduce: combine the values associated with each key
      |
      v
Output partitions
```

This separation makes distributed processing more accessible. It does not eliminate engineering judgement: developers still need correct keys, sensible partitioning, valid aggregation logic, and suitable handling of retries and external side effects.

A cluster does not survive failures automatically merely because it has several nodes. Its framework, storage, and control services need appropriate recovery and availability design.

For the original model and its division of responsibilities, see [Dean and Ghemawat's MapReduce paper](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/).

## 5. When distribution is unnecessary

Prefer a single-machine solution when it meets memory, throughput, deadline, and reliability requirements at acceptable cost.

Distribution introduces scheduling and network overhead, a larger operational surface, and more difficult debugging. It may take longer than local processing for a small job.

However, “fits in RAM” does not prove that a single machine is always fastest or sufficient. A compute-heavy job, many simultaneous users, a strict deadline, or availability requirements may still justify additional machines.

A useful decision sequence is:

1. Define the workload and service requirements.
2. Measure the current bottleneck.
3. Check efficient single-machine options.
4. Estimate partitionability, communication, and operating costs.
5. Distribute when the measured benefits justify those costs.

Classic MapReduce is primarily a batch-processing model. A live high-rate stream usually needs an appropriate streaming architecture; “use a cluster” does not by itself select the right processing system.

## 6. Worked practice

### Practice 1 — Diagnose the Vs

| Workload | Dominant V | Reason |
| --- | --- | --- |
| Ten years of a bank's transactions | Volume | A potentially large historical collection must be stored and queried |
| Five million sensor readings per second | Velocity | Processing must keep pace with the arrival rate |
| Text reviews, images, and clickstream JSON together | Variety | Sources have different representations and processing requirements |
| A 5,000-row marks spreadsheet | Usually none at a big-data scale | Routine tools can normally handle this workload |

Historical transaction data is not automatically beyond one machine; its actual size and queries determine the architecture. Similarly, multiple formats do not alone establish the need for a cluster.

A small marks sheet illustrates that “big” is relative to the processing requirements and available tools rather than a fashionable label.

### Practice 2 — Find the vertical-scaling wall

1. **Physical ceiling:** the platform has finite memory slots, processor capacity, storage connections, and bandwidth.
2. **Financial ceiling:** a larger server may cost more than the workload benefit warrants; compare actual configurations and operating costs.
3. **Operational risk:** failure of the only active host stops its work until recovery or failover.
4. **Change of strategy:** consider horizontal scaling when a suitable single-machine approach cannot meet capacity, deadline, or reliability needs economically.

Fault tolerance can justify redundancy before data exceeds one machine's capacity. That decision still needs a recovery design, not merely extra hardware.

### Practice 3 — Weigh a 20-node cluster

| Potential gains | New or expanded problems |
| --- | --- |
| More aggregate storage and memory | Partition data without excessive skew |
| More parallel throughput | Schedule and coordinate tasks |
| Incremental capacity growth | Recover from partial node failures |
| Recovery options through redundant storage and retries | Transfer intermediate results over the network |
| Possible cost advantages | Operate and monitor more machines |

For a report joining two large tables, partitioning and data movement are especially important. Rows with the same join key must be brought together or accessed efficiently, and uneven key frequencies can leave one worker doing much more work than the others.

These are potential gains, not guaranteed savings or speedups.

### Practice 4 — Choose a single machine or distributed system

| Scenario | Initial choice | Justification |
| --- | --- | --- |
| A 2 GB CSV already shown to load comfortably on a 16 GB laptop | Single machine | The stated workload fits the existing tools; measure peak memory during transformations |
| Parse and count 500 TB of web-crawl data | Distributed storage and processing are a strong candidate | Volume and full-scan throughput likely exceed an ordinary workstation's practical limits |
| Summarise and plot a 50,000-row survey | Single machine | Routine analysis usually does not justify cluster overhead |
| Process ten million events per second in real time | Evaluate a distributed streaming system | Sustained ingestion and processing likely need parallel capacity; event size and per-event work matter |

There is no universal rule that 500 TB cannot be stored on any single system or that an event count alone determines capacity. These recommendations follow the exercise's ordinary-machine assumptions and must be confirmed against measured requirements.

**Rule:** choose distribution to solve an actual capacity, time, or reliability problem, after considering its overhead.

### Practice 5 — Explain the value of the abstraction

1. Without a framework, programmers must implement partitioning, coordination, fault recovery, and inter-machine data movement.
2. Correctness requires handling concurrency, partial failure, retries, and network behaviour, which is substantial systems work beyond the analysis itself.
3. “Write two functions” means supplying the transformation and aggregation logic while the runtime manages much of the distributed execution.
4. The abstraction lets more teams work on the data question instead of implementing a distributed runtime for every project.

Frameworks reduce the burden but do not prove that a task is suitable for MapReduce. The next lesson can focus on expressing the computation through map and reduce once this architectural trade-off is understood.

## 7. Theory exercises — suggested answers

These are study references. Use your own explanations and examples for course submissions.

### Task 1 — Defining the three Vs

- **Volume:** the amount of data that must be stored and processed. For example, a national astronomy project may collect a long-term archive of telescope observations too large for an ordinary workstation to analyse efficiently.
- **Velocity:** how quickly data arrives and how quickly it must be handled. For example, a nationwide payment network must analyse continuous card-authorisation requests without an unacceptable queue.
- **Variety:** the diversity of formats and structures. For example, a hospital research project might combine clinical notes, medical images, laboratory tables, and appointment records.

These examples identify different pressures. The required resources and analysis determine whether they need distribution.

### Task 2 — Vertical scaling limitations

Vertical scaling increases one machine's capacity, but its platform has finite limits on RAM, processors, and I/O. High-capacity hardware can also become too expensive relative to the extra performance it provides.

Relying on one unprotected machine creates an operational risk: if it fails, the workload stops until recovery. Horizontal scaling can address capacity and recovery requirements, but only with suitable partitioning, redundant data, and fault-handling mechanisms.

### Task 3 — Horizontal scaling challenges

**Partitioning:** a single-machine program can access its local data without assigning it to separate networked hosts. A cluster must distribute records so workers have manageable, reasonably balanced partitions. Poor partitioning can overload one node or force unnecessary transfers. Local parallel programs can also partition data, but the cluster adds placement and network concerns.

**Data movement:** a single machine moves data through its own memory and storage system. A cluster may need to send records between machines, adding serialisation, network delay, and bandwidth limits. A large join can be particularly costly when matching records begin on different nodes.

These concerns exist locally in simpler forms; they become more visible and expensive across a cluster.

### Task 4 — The value of MapReduce

MapReduce separates analysis logic from much of the distributed execution machinery. The programmer specifies map and reduce functions, while the framework organises input tasks, schedules workers, groups intermediate records by key, transfers results, and handles supported task failures.

Its value is making suitable large batch computations accessible without requiring every analyst to build a distributed system. Programmers still need correct logic and an understanding of the workload's costs.

### Task 5 — Distribution decision analysis

A 10 GB dataset that fits comfortably in the workstation's 32 GB RAM does not justify a cluster merely because someone calls it a big-data project. Start with the workstation and measure peak working memory and runtime.

A cluster introduces task startup, communication, coordination, deployment, and debugging costs. For a workload the workstation already handles within the required time, those costs can make the project slower and harder to maintain.

Distribution becomes worth considering if measurements reveal an unmet processing deadline, insufficient throughput, expected growth, or a separate availability requirement. Dataset size alone is not enough.

## 8. Quick revision

- Volume concerns amount; velocity concerns arrival rate; variety concerns different forms.
- “Big” is relative to resources and requirements.
- Scale up by enlarging one machine; scale out by adding machines.
- Aggregate cluster memory is not one shared memory space.
- More nodes require partitioning, coordination, fault recovery, and data movement.
- Cluster cost, resilience, and speedup depend on design and workload.
- Try efficient local tools before adding distributed complexity.
- MapReduce abstracts suitable distributed batch computations; it is not every workload's answer.

## Sources

- User-supplied course material: *Data Science and Analytics, Module V: Data Modeling with the MapReduce Paradigm, Big Data and Distributed Computing*.
- [Dean and Ghemawat: MapReduce — Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) — original programming model and runtime responsibilities.
- [Apache Hadoop: MapReduce Tutorial](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html) — framework overview and execution concepts.

Worked responses and clarifying notes were prepared for this repository.

[Module overview](./README.md) · [Theory index](../README.md)
