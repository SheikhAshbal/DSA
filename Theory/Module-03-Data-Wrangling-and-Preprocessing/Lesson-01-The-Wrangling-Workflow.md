# Lesson 1: The Wrangling Workflow — Assess, Structure, Clean, Munge

[Theory index](../README.md) · [Module overview](./README.md)

**Course:** Data Science and Analytics  
**Module III:** Data Wrangling and Preprocessing  
**Estimated study time:** 45 minutes

## Learning objectives

- Define data wrangling and explain its role in the data science lifecycle.
- Identify the four wrangling activities and their outputs.
- Assess quality and tidiness issues before changing a dataset.
- Explain why wrangling must be documented and reproducible.

## 1. What is data wrangling?

Data wrangling transforms raw data into a structured, reliable form suitable for analysis. It includes inspecting data, reshaping tables, resolving quality issues, and preparing the final representations an analysis requires. The term *munging* can refer to wrangling generally; this lesson uses it more narrowly for the final transformation activity.

A typical lifecycle places wrangling after data collection and before detailed analysis or modelling. In practice, it is iterative: later discoveries can require another assessment or cleaning pass.

The principle **garbage in, garbage out** explains why wrangling matters. A model can learn from incorrect scores, duplicate records, or misinterpreted dates without detecting their real-world meaning. Sophisticated modelling cannot make unreliable inputs trustworthy.

### The lesson's illustrative time budget

| Activity | Hours in a hypothetical 100-hour project |
| --- | ---: |
| Assessment | 10 |
| Structuring | 12 |
| Cleaning | 25 |
| Munging / transforming | 13 |
| Total wrangling | 60 |
| Other project activities | 40 |

This example illustrates how much effort preparation can require. The lesson's broader 60–80% estimate is a teaching guideline, not a fixed proportion for every project.

## 2. The four wrangling activities

| Activity | Main question | Typical output |
| --- | --- | --- |
| Assessment | What is wrong, uncertain, or unsuitable? | A documented list of quality and tidiness issues |
| Structuring | Does the table represent the observational units correctly? | A tidy table or related tidy tables |
| Cleaning | Are the values valid, consistent, and sufficiently complete? | Values corrected or explicitly flagged under documented rules |
| Munging / transforming | Does the data have the form the analysis needs? | Analysis-ready data with appropriate types and representations |

```text
Raw data
   |
   v
Assess -> Structure -> Clean -> Transform -> Validate
   ^                                         |
   |________ Revisit issues when needed _____|
```

These activities overlap. For example, diagnosing malformed dates is assessment; resolving invalid date strings is cleaning; converting valid dates into date objects is transformation.

### Why assessment comes first

1. **It establishes what needs fixing.** Inspect the schema, types, ranges, missing values, duplicates, formats, and unusual records before deciding on a rule.
2. **It preserves evidence.** Premature changes can hide the original problem or replace a suspicious value with an unsupported guess.

Keep an unchanged raw copy and an issue log. For each issue, record the affected field or records, the evidence, the proposed rule, and any decision that still needs confirmation.

### Classifying common problems

| Problem | Main activity | Reason |
| --- | --- | --- |
| Two identical user/time/action records | Cleaning, after investigation | Remove only if they are confirmed unintended duplicates |
| Months stored in separate columns | Structuring | Move month labels into a month column |
| Scores such as `88%`, `72 %`, and `n/a` | Cleaning, then transformation | Standardize representations, identify missing values, then convert to numeric form |
| Dates needed as date objects | Munging / transforming | Parse validated strings into the required type |
| A combined name field when separate components are required | Structuring | Split according to a documented rule; real names may require more than splitting on a space |

## 3. Tidy data: the target structure

Tidy data follows three rules:

1. Each variable is a column.
2. Each observation is a row.
3. Each type of observational unit is a table.

The observational unit depends on the question. For monthly student scores, one observation is a **student-month** measurement.

### Wide input

| student | sep | oct |
| --- | ---: | ---: |
| Ali | 88 | 90 |
| Sara | 72 | 75 |

### Tidy long output

| student | month | score |
| --- | --- | ---: |
| Ali | sep | 88 |
| Ali | oct | 90 |
| Sara | sep | 72 |
| Sara | oct | 75 |

Here, month is a variable whose values were encoded in column headings. Moving those values into one column gives each measurement its own row.

Tidy structure is relative to the intended observations. Wide tables can be useful for presentation or certain model inputs; the long form is the appropriate target for this lesson's repeated monthly measurements.

Students and submissions are different unit types. A student table can contain one row per student, while a submissions table contains one row per submission linked by a student identifier.

## 4. Reproducible wrangling

Every transformation should live in code that can be reviewed and run again. Preserve raw input, document decisions, record relevant dependencies, and generate cleaned output separately.

| Situation | Risk of unrecorded manual edits | Benefit of a script |
| --- | --- | --- |
| Next month's data arrives | Repeating edits takes time and may produce different results | Apply the same rules and validation checks |
| A reviewer questions a changed score | The reason and original value may be lost | Inspect the rule and its documented evidence |
| A date correction contains a bug | Finding and reversing all edits is difficult | Fix the rule and regenerate from raw input |
| A teammate reproduces the work | Hidden steps prevent the same result | Share input, code, settings, and environment information |

Code alone does not justify a decision. A script that replaces `720` with `72` still needs evidence for that correction. Reproducibility requires both repeatable operations and documented reasoning.

## 5. Worked practice

### Practice 1 — Assess before fixing

#### Raw sample

| id | name | batch | score | joined |
| --- | --- | --- | --- | --- |
| 1 | Ali | 23BSCYS | 88 | 2025-09-01 |
| 2 | ali | 23BSCYS | 88 | 2025-09-01 |
| 3 | Sara | 23-BSCYS | 720 | 01/09/2025 |
| 4 | Bilal | *(blank)* | -5 | not sure |
| 5 | Zoya | 23BSCYS | *(blank)* | 2025-13-40 |

#### Assessment log — no values changed

| Field / records | Finding | Decision or evidence needed |
| --- | --- | --- |
| Names in records 1 and 2 | Capitalization differs | Establish a display or comparison convention |
| Records 1 and 2 | Potential duplicate: name differs only by case and other non-ID values match | IDs differ, so these are not exact duplicate rows; verify identity before removing either |
| Batch in record 3 | `23-BSCYS` differs from `23BSCYS` | Confirm the canonical batch format |
| Batch in record 4 | Missing | Consult the source or retain an explicit missing value |
| Score in record 3 | `720` is outside a presumed 0–100 range | Confirm the score scale and original result; do not assume the intended score is 72 |
| Score in record 4 | `-5` is invalid under a 0–100 rule | Check whether it is an error or a documented sentinel value |
| Score in record 5 | Missing | Choose a justified missing-data policy |
| Joined in records 1–3 | Mixed date representations | Confirm source conventions before parsing |
| Joined in record 3 | `01/09/2025` is ambiguous | Confirm whether it means 1 September or 9 January |
| Joined in record 4 | `not sure` is not a usable date | Investigate or represent as missing with an issue flag |
| Joined in record 5 | `2025-13-40` is not a valid calendar date | Check the source; never invent a replacement |
| Schema | Actual storage types cannot be established from a printed table | Inspect the loaded dataset's types |

The table already has one apparent student record per row and one field per column. There is no demonstrated need to reshape it. A batch code need not be split unless the analysis requires its components.

**Why assess first?** Recording these findings before editing preserves the original evidence and prevents assumptions from becoming silent corrections.

### Practice 2 — Map issues to activities

| Issue | Activity / treatment |
| --- | --- |
| Finding and recording all issues | Assessment |
| Potential duplicate records | Cleaning after identity verification |
| Inconsistent batch and name formatting | Cleaning under documented conventions |
| Out-of-range scores | Cleaning: verify, correct from evidence, or flag |
| Missing batch, score, or date values | Cleaning under an explicit missing-data policy |
| Mixed and invalid date strings | Cleaning to resolve representations and invalid values |
| Conversion of validated dates to date objects | Munging / transforming |
| Need for a different observational unit or separate required fields | Structuring, if assessment establishes the need |

**Order:** preserve raw input → assess → structure if needed → clean → transform → validate.

This sample does not require reshaping merely to satisfy the workflow. In a different dataset, restructuring first may expose missing observations or duplicates at the correct unit of analysis. Conversely, malformed values may need cleaning before a reshape can succeed. Assessment determines the defensible order, and the workflow can repeat.

An ordered plan makes each change deliberate and reviewable instead of a series of disconnected edits.

### Practice 3 — Reshape monthly scores

This example uses only the Python standard library.

```python
wide = {
    "student": ["Ali", "Sara"],
    "sep": [88, 72],
    "oct": [90, 75],
}

tidy = []
for i, student in enumerate(wide["student"]):
    for month in ("sep", "oct"):
        tidy.append({
            "student": student,
            "month": month,
            "score": wide[month][i],
        })

for row in tidy:
    print(row)
```

Expected output:

```text
{'student': 'Ali', 'month': 'sep', 'score': 88}
{'student': 'Ali', 'month': 'oct', 'score': 90}
{'student': 'Sara', 'month': 'sep', 'score': 72}
{'student': 'Sara', 'month': 'oct', 'score': 75}
```

Grouping by the month column now gives September's mean as `(88 + 72) / 2 = 80` and October's as `(90 + 75) / 2 = 82.5`. The same month and score columns can support a plot without separate logic for each month's column. For chronological plotting across years, use a proper year-month value.

### Practice 4 — Explain reproducibility

1. **New monthly data:** manual work must be repeated; a script applies the established rules to the new input and reports new validation failures.
2. **A questioned score correction:** an unrecorded edit may have no explanation; a documented script identifies the change and its supporting evidence. Without evidence, 720 remains flagged rather than silently becoming 72.
3. **A date-processing bug:** manual repairs are hard to trace; a script can be corrected and rerun from unchanged raw data.
4. **A teammate reproducing the result:** manual steps may be omitted or interpreted differently; shared inputs, code, configuration, and pinned dependencies support the same result.

This follows the lesson's reproducibility rule and the lab habit of recording the environment needed to rerun the work.

### Practice 5 — An assessment-first checklist

- [ ] Preserve an unchanged copy of the raw input and record its source.
- [ ] Define the intended analysis, observational unit, schema, and valid ranges.
- [ ] Inspect types, dimensions, missingness, duplicates, formats, ranges, and unusual values.
- [ ] Write an issue log before changing any values; distinguish confirmed errors from suspicions.
- [ ] Plan the rules and identify decisions that need source verification.
- [ ] Structure the data toward one variable per column, one observation per row, and one unit type per table.
- [ ] Clean inconsistent, invalid, missing, and duplicate values using documented rules.
- [ ] Transform types and representations into the form required by the analysis.
- [ ] Implement every change in rerunnable code and record relevant dependencies.
- [ ] Validate row counts, keys, ranges, types, missingness, and relationships; explain any remaining exceptions.
- [ ] Save the derived output separately and confirm it can be regenerated from the raw input.

**Rule I would never break:** assess and document the issues before changing the data.

An assessment-first plan connects each operation to an observed problem and a stated purpose.

## 6. Theory exercises — suggested answers

These answers are study references based on the supplied lesson.

### Task 1 — Defining data wrangling

Data wrangling is the process of assessing, restructuring, cleaning, and transforming raw data so it is suitable for analysis. It connects data collection with reliable exploration and modelling. Under the garbage-in, garbage-out principle, errors in the input can lead to misleading results even when the model itself works correctly. Wrangling helps ensure that later analysis uses meaningful records, valid values, and appropriate representations.

### Task 2 — The four activities and their outputs

| Activity | Output |
| --- | --- |
| Assessment | A written inventory of quality and tidiness issues |
| Structuring | Tidy tables representing the intended observational units |
| Cleaning | Corrected, standardized, or explicitly flagged values |
| Munging / transforming | Data in the final types and representations required for analysis |

### Task 3 — The importance of prior assessment

Cleaning or structuring before assessment is a beginner error for two reasons. First, without inspecting the data and its meaning, the analyst may apply the wrong correction, remove legitimate records, or reshape around the wrong unit of observation. Second, premature edits can hide the original evidence and make it difficult to explain what changed. Assessment creates a documented basis for choosing and reviewing the transformations.

### Task 4 — Identifying tidy data

In `PatientID, January_BP, February_BP, March_BP`, the month values are embedded in column names. For an analysis of monthly blood pressure measurements, each observation should represent one patient in one month.

The tidy columns should therefore be:

| PatientID | Month | BloodPressure |
| --- | --- | --- |
| P001 | January | 120 |
| P001 | February | 118 |
| P001 | March | 122 |

*The values above are illustrative.*

Each variable has one column, each patient-month measurement has one row, and all blood pressure measurements belong to one observational-unit table. Patient-level attributes can be stored in a separate patient table linked through PatientID. Include the year when the data spans multiple years.

### Task 5 — Reproducibility in wrangling

Manual spreadsheet edits carry three main risks:

1. **Inconsistent repetition:** fresh data requires repeating the work, and the same decisions may be applied differently.
2. **Weak traceability:** without a change record, it is difficult to explain which value changed and why.
3. **Difficult recovery and collaboration:** a mistake may require many edits to reverse, and a teammate may be unable to recreate the result.

A version-controlled script records the operations, can be corrected and rerun from raw input, and can be shared with the required environment information. Documented rules and evidence explain why each operation is justified.

## 7. Quick revision

- **Assess:** discover and document issues before editing.
- **Structure:** represent variables and observations in suitable tables.
- **Clean:** resolve value problems using evidence and explicit rules.
- **Transform:** prepare the types and representations the analysis needs.
- **Validate:** check that the output satisfies the documented requirements.
- A suspected duplicate is not automatically a confirmed duplicate.
- An invalid value is a reason to investigate, not permission to guess.
- Keep raw data unchanged and make the workflow reproducible.

## Source

Adapted and expanded from the user-supplied course material: *Data Science and Analytics, Module III: Data Wrangling and Preprocessing, Lesson 1: The Wrangling Workflow: Assess, Structure, Clean, Munge*. Worked responses and clarifying notes were prepared for this repository.

[Back to module overview](./README.md) · [Back to Theory](../README.md)
