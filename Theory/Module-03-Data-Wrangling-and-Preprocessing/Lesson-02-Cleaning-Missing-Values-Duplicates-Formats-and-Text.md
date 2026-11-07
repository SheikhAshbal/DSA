# Lesson 2: Cleaning — Missing Values, Duplicates, Formats and Text

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-01-The-Wrangling-Workflow.md)

**Course:** Data Science and Analytics  
**Module III:** Data Wrangling and Preprocessing  
**Estimated study time:** 55 minutes

## Learning objectives

- Choose an appropriate missing-data treatment and explain its trade-offs.
- Distinguish accidental duplicates from legitimate repeated events.
- Convert inconsistent representations to a canonical format.
- Explain and apply text normalisation and extraction.
- Order cleaning steps so that one operation does not undermine another.

## 1. Missing data: investigate before deciding

A blank value is a finding, not an instruction to delete or fill it. First investigate how much is missing, which records are affected, and why the values are absent.

| Strategy | What it does | Main risk |
| --- | --- | --- |
| Drop rows | Excludes observations with missing required values | Loses information and can bias results if excluded records differ systematically |
| Drop a column | Excludes a variable | Removes potentially useful information |
| Impute | Replaces missing entries using a stated rule, such as a median, mode, or model | Introduces estimates that can distort distributions and relationships |
| Preserve and flag missingness | Retains the absence and records its meaning where known | Leaves a gap that some analyses cannot directly use; may need additional handling |

Imputation estimates an unknown value; it does not recover the original observation. Simple mean or median replacement can reduce apparent variation and conceal uncertainty.

### Why the cause matters

A score lost through a quiz-system failure is different from an absent submission timestamp for someone who never submitted. The first is an unobserved measurement; the second may represent the absence of an event.

A refusal to disclose income may itself carry information. Do not automatically replace it with a typical income, or treat “declined” as a numeric amount. Preserve the numeric field as missing and record a separate reason or indicator when appropriate.

The lesson describes a random system failure as “missing at random.” More precisely, missingness unrelated to observed and unobserved values is *missing completely at random*; the broader *missing at random* condition can depend on observed information. Neither a small missing percentage nor a label alone guarantees a treatment is unbiased.

## 2. Duplicates: identify the observation and its key

An **accidental repeat** records the same real observation more than once. A **legitimate repeat** records another real observation, even when some or all recorded attributes match.

| Example | Interpretation |
| --- | --- |
| A confirmed logging retry stores the same event twice | Remove the accidental extra record |
| The same user logs in at 03:14 and 09:00 | Keep both events |
| Two separate orders contain the same item, customer, and date | Keep both if they are separate purchases |
| Two identical rows lack an event or order ID | Investigate; equality alone does not establish duplication |

Choose a key that identifies the intended observational unit. A user ID identifies a person, not necessarily a unique login, review, or purchase.

For the lesson's toy log dataset, the key is **(user, timestamp, action)**. In a production dataset, timestamp precision, date, timezone, and event identifiers may also matter.

### Normalise before comparing, then verify

Values such as `" Ali"` and `"ali"` do not compare equally until a suitable comparison rule is applied. Normalisation can expose candidate duplicates, but matching names do not prove that two people are the same.

Use field-specific rules. Lowercasing a location label may be appropriate; lowercasing an identifier could merge distinct IDs if its system treats case as significant.

## 3. Inconsistent formats

The same batch may appear as `23BSCYS`, `23-BSCYS`, `23 bscys`, or `23bscys`.

Inconsistent representations can cause:

- **Grouping errors:** one real category appears as several groups.
- **Sorting errors:** date strings may sort alphabetically rather than chronologically.
- **Join failures:** matching records fail to connect because their keys differ in spacing, case, or format.

### Canonicalisation workflow

1. Inspect the variants and confirm which represent the same value.
2. Define a canonical representation for each field.
3. Apply a documented mapping or parsing rule.
4. Flag values the rule cannot interpret.
5. Validate the results and retain the original input.

For batch codes, the course example removes approved separators and uses uppercase. Do not remove punctuation indiscriminately from every field.

For dates, resolve ambiguous values such as `01/09/2025` using the source convention before parsing. Use actual date objects for chronological operations; choose a consistent format when exporting them.

## 4. Text normalisation and extraction

| Operation | Meaning | Example |
| --- | --- | --- |
| Normalisation | Makes equivalent representations consistent | Trim and lowercase `" New York "` to `"new york"` |
| Extraction | Pulls a required value from a larger string | Extract `91` from `"score: 91"`, then convert it to an integer |

Normalisation may include trimming surrounding whitespace, applying a case convention, and removing known irrelevant separators. Extraction may use a parser or regular expression.

Missing, malformed, and out-of-range values are different conditions. Keeping an issue flag helps distinguish them even when the numeric result is missing in each case.

## 5. Worked practice

### Practice 1 — Choose a missing-data treatment

| Situation | Defensible treatment | Reason and trade-off |
| --- | --- | --- |
| Score missing for 2% because of random quiz glitches | For an illustrative analysis, use a documented mean or median estimate if appropriate and flag imputed entries | Retains rows, but reduces variation and does not recover actual scores; do not use estimated values as official grades |
| Income missing for 40% because people declined | Preserve missing income and record “declined”; consider excluding the variable if it cannot support the intended analysis | Refusal is meaningful, and filling many values could hide the pattern; dropping the variable also loses information |
| Batch missing for 1 of 500 records | Check the source first; if unrecoverable and batch is required, excluding that row may be reasonable | Small numerical loss, but still inspect whether the row is unusual; preserve it for analyses that do not need batch |
| Submission time blank for non-submitters | Keep the timestamp missing and record a submitted/not-submitted indicator | There is no submission time to invent |

Knowing why a value is absent helps distinguish an unknown measurement from meaningful non-response or the absence of an event.

### Practice 2 — Remove only confirmed accidental repeats

Assume the first two records are confirmed copies of one event.

```python
rows = [
    {"user": "ali", "ts": "03:14", "action": "login"},
    {"user": "ali", "ts": "03:14", "action": "login"},
    {"user": "ali", "ts": "09:00", "action": "login"},
]

seen, unique = set(), []
for row in rows:
    key = (row["user"], row["ts"], row["action"])
    if key not in seen:
        seen.add(key)
        unique.append(row)

print(len(rows), "->", len(unique), "rows")
for row in unique:
    print(row)
```

Expected output:

```text
3 -> 2 rows
{'user': 'ali', 'ts': '03:14', 'action': 'login'}
{'user': 'ali', 'ts': '09:00', 'action': 'login'}
```

Using only `user` as the key would incorrectly delete the genuine 09:00 login.

### Practice 3 — Standardise batch codes

For this known batch-code convention, spaces and hyphens are irrelevant separators.

```python
raw = ["23BSCYS", "23-BSCYS", "23 bscys ", "23bscys", "22BSCYS"]

def canon(batch):
    return batch.strip().upper().replace("-", "").replace(" ", "")

cleaned = [canon(batch) for batch in raw]
print("raw distinct:", len(set(raw)))
print("cleaned distinct:", len(set(cleaned)))
print(cleaned)
```

Expected output:

```text
raw distinct: 5
cleaned distinct: 2
['23BSCYS', '23BSCYS', '23BSCYS', '23BSCYS', '22BSCYS']
```

There are exactly five distinct raw strings and two canonical batch codes. Canonicalisation prevents the same batch from being split across separate groups before counting students.

### Practice 4 — Extract numeric scores

The course example searches for the first sequence of digits:

```python
import re

raw = [" 88% ", "72 %", "n/a", "score: 91", ""]
values = []
for text in raw:
    match = re.search(r"\d+", text)
    values.append(int(match.group()) if match else None)

print("parsed:", values)
numbers = [value for value in values if value is not None]
mean = sum(numbers) / len(numbers) if numbers else None
print("mean of valid:", mean)
```

Expected output:

```text
parsed: [88, 72, None, 91, None]
mean of valid: 83.66666666666667
```

The mean uses only the three parsed values: `(88 + 72 + 91) / 3`.

**Normalisation versus extraction:** the regular-expression search extracts digits and ignores surrounding characters; it does not explicitly normalise the whole string. Calling `text.strip().lower()` would be an explicit normalisation step.

**Limits of this teaching example:** the pattern would extract 5 from `"-5"`, 88 from `"88.5"`, and 88 from `"88 out of 100"`. It does not validate the full input or the 0–100 range. Use a parser that matches the allowed full format, handles signs and decimals as required, and validates the resulting number before accepting it.

These percentage scores are represented in percentage points: 88 means 88%. If an analysis requires a proportion, convert it explicitly to 0.88.

Keeping `None` when no value can be parsed is safer than guessing a score. Record the reason for failure so that malformed inputs can be reviewed.

### Practice 5 — Order the operations

Input:

| name | batch | score |
| --- | --- | --- |
| `' Ali'` | 23-BSCYS | `'88%'` |
| `'ali'` | 23BSCYS | `'88%'` |
| `'Sara'` | 23 bscys | `'n/a'` |

A defensible sequence is:

1. **Assess and preserve:** retain the raw table and document the intended observation and duplicate key.
2. **Normalise names and batch formats:** trim whitespace, apply approved comparison casing, and standardise batch separators.
3. **Parse and validate scores:** convert `88%` to numeric 88; represent `n/a` as missing under the documented rule.
4. **Review and remove confirmed duplicates:** the two Ali records now match on the available fields. In this exercise they can be treated as copies if that assumption is stated; real student data needs a reliable identifier or source confirmation.
5. **Handle remaining missing scores:** retain a flag, recover the value, exclude the observation for a particular analysis, or impute under a justified policy.
6. **Validate:** check counts, score ranges, missingness, canonical categories, and key uniqueness.

Duplicate comparison belongs after normalisation because unnormalised spelling variants can hide the match. Removing confirmed duplicate copies before computing an imputation statistic also prevents those copies from receiving extra weight. Do not impute first and then infer identity from values that the imputation created.

The order can change when data constraints require it; the purpose is a documented and reproducible sequence.

## 6. Theory exercises — suggested answers

These are study references. Use your own explanation and examples when completing course submissions.

### Task 1 — Missing data trade-offs

Dropping removes rows or columns containing missing values. It is simple, but it discards information and may bias the results if the excluded records differ from those retained.

Imputation replaces missing entries with estimates, such as a median, mode, or model prediction. It preserves more rows, but the replacement is not an observed value and can distort variation or relationships.

The cause of missingness is critical. A value lost through a random technical fault may justify a different treatment from income withheld deliberately or a timestamp absent because an event never happened. Investigating the cause helps us choose a treatment and explain its limitations.

### Task 2 — Identifying true duplicates

An accidental repeat is an extra record of the same observation, while a legitimate repeat represents another real observation.

For example, a shop could sell two identical notebooks to the same customer in separate transactions within one minute. If the dataset stores only customer, product, price, and a timestamp rounded to the minute, the rows could look identical even though both sales happened. Removing one would undercount sales.

Check transaction identifiers and source records before treating matching rows as accidental copies.

### Task 3 — Impact of inconsistent formats

Inconsistent formats can split one category into several groups, put date strings in the wrong chronological order, and prevent matching records from joining.

For example, `23BSCYS` and `23-BSCYS` could be counted as different batches even though they refer to the same batch.

The fix is to define a canonical format for each field and convert equivalent representations to it using documented rules. This might involve trimming whitespace, applying consistent case, removing approved separators, or parsing dates under a confirmed date convention. Validate the results and flag values that cannot be interpreted.

### Task 4 — Text normalisation versus extraction

Normalisation makes different representations of the same value consistent. For example, trimming spaces and converting `" NEW YORK "` to lowercase produces `"new york"`.

Extraction pulls a particular piece of information from a string. For example, extracting `91` from `"score: 91"` and converting it to an integer produces a value that can be used in calculations.

Normalisation standardises the representation; extraction retrieves the required content. Both need rules appropriate to the field.

### Task 5 — Applied cleaning strategy

| Column | Cleaning action | Justification |
| --- | --- | --- |
| Rating | Inspect the number and cause of blanks, keep missingness explicit, and validate observed ratings as 1–5. If a numeric input is required, choose and document a justified exclusion or imputation policy | A blank is not a zero rating. Automatic filling can distort customer sentiment, while dropping records loses information |
| User ID and repeated reviews | Investigate records matching on user ID, timestamp, and review text. Remove confirmed duplicate copies using that composite key or a reliable review ID | A user can legitimately write multiple reviews, so removing repeats by user ID alone would delete real data |
| Location | Trim whitespace and map `New York`, `new york`, and `NEW YORK` to one canonical label, such as `New York` | Equivalent locations should group and join consistently |

Normalise the relevant comparison fields before duplicate detection, verify the event identity, and resolve confirmed duplicates before calculating any replacement-rating statistic. Preserve the raw data and record every operation in rerunnable code.

## 7. Quick revision checklist

- [ ] Investigate why values are missing before choosing a treatment.
- [ ] Distinguish unknown values from events that never occurred.
- [ ] Choose duplicate keys based on the observational unit.
- [ ] Keep legitimate repeated events.
- [ ] Apply field-specific canonical formats.
- [ ] Separate normalisation from extraction.
- [ ] Validate parsed values instead of accepting any digits found.
- [ ] Record decisions and regenerate cleaned output from unchanged raw input.

## Source

Adapted and expanded from the user-supplied course material: *Data Science and Analytics, Module III: Data Wrangling and Preprocessing, Cleaning: Missing Values, Duplicates, Formats and Text*. Worked responses and clarifying notes were prepared for this repository.

[Previous lesson](./Lesson-01-The-Wrangling-Workflow.md) · [Module overview](./README.md) · [Theory index](../README.md)
