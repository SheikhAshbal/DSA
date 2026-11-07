# Lesson 3: Dashboards and Storytelling with Data

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-02-Choosing-the-Right-Plot-and-Tools.md)

**Course:** Data Science and Analytics  
**Module VII:** Data Visualization  
**Estimated study time:** 45 minutes

## Learning objectives

- Distinguish exploratory and explanatory visualisation.
- Organise a data story around context, evidence, and a decision.
- Design monitoring views from audience questions.
- Tailor detail without changing facts or hiding material caveats.
- Turn analysis into a clear recommendation or responsible next investigation.

## 1. Exploratory and explanatory visuals

| Dimension | Exploratory | Explanatory |
| --- | --- | --- |
| Primary audience | Analyst or team investigating the data | People who need to understand a finding or make a decision |
| Goal | Discover patterns, questions, and problems | Communicate selected findings with context |
| Typical output | Many provisional charts and comparisons | A smaller, curated set with clear labels and annotations |
| Quality requirement | Correct enough to support investigation | Correct, readable, contextualised, and appropriate to the audience |

“Rough” does not mean inaccurate. An exploratory plot still needs valid inputs and meaningful scales. A polished figure can also be exploratory when it supports open-ended investigation.

The course's “100 exploratory charts to one presented chart” is an illustration of selection, not a required quota. Some findings need several complementary visuals.

Do not send an audience the whole search history when they need a conclusion. Keep the underlying analysis and supporting material available for audit or technical follow-up.

## 2. Give the evidence a narrative structure

The course uses:

```text
Setup -> Conflict -> Resolution
Context -> Important finding -> Recommended decision or next step
```

| Part | Question it answers | What to include |
| --- | --- | --- |
| Setup | Why are we looking at this? | Audience, problem, scope, population, and question |
| Conflict | What important issue does the evidence reveal? | The finding and the few charts needed to support it |
| Resolution | What should happen next? | A proportionate action, owner, evaluation plan, and relevant limitations |

A conflict need not be sensational. It may be a gap, an unexpected pattern, or a decision that now needs evidence.

A resolution does not require pretending the question is settled. When the evidence is uncertain, checking the data or running a pilot can be the appropriate recommendation.

### Keep the reasoning visible

Distinguish:

- **Observation:** what the data shows.
- **Interpretation:** the explanation supported or suspected.
- **Recommendation:** what action is justified.
- **Evaluation:** how to check whether the action helped.

A persuasive sequence is not permission to cherry-pick evidence or remove findings that weaken the preferred conclusion.

## 3. Dashboard or one-off story?

| Need | Suitable format | Reason |
| --- | --- | --- |
| Explain one completed investigation | Report, presentation, or explanatory figure | A fixed narrative guides a particular decision |
| Monitor recurring questions | Dashboard | Repeated access to a consistent set of metrics |
| Investigate an emerging issue | Exploratory workspace or focused diagnostic view | The next question may change as evidence appears |

A dashboard can use live, scheduled, or manually refreshed data. It is not defined by guaranteed real-time updates. Show the data-as-of time, refresh status, and scope so users can judge whether it is current enough.

Design from questions, not available chart types:

1. Identify the audience and its recurring decisions.
2. Define each decision's metric and unit of analysis.
3. State denominators, time windows, filters, and update cadence.
4. Choose the smallest useful set of views.
5. Put the highest-priority information prominently.
6. Test whether the intended user can find a next action.

A dashboard may combine explanatory headlines with exploratory interactions. The distinction is about its purpose, not a rigid technical boundary.

[Tableau's dashboard guidance](https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm) similarly emphasises purpose, audience, hierarchy, and limiting competing views.

## 4. The “everything dashboard” failure

An everything dashboard includes many panels because the data exists, rather than because a user needs them.

Typical symptoms include:

- Important counts competing with decorative or low-priority charts.
- Several charts repeating essentially the same information.
- Undefined rates with changing denominators.
- Filters whose effects are unclear.
- No clear freshness indicator or follow-up action.
- Tiny panels that become unreadable on the actual display.

The solution is not an arbitrary maximum number of charts. Prioritise questions, combine or remove redundant views, and move specialist diagnostics to a detail page.

A teacher-admin may need an approval queue, a behind-schedule worklist, and lesson bottlenecks. Browser share is useful only when it answers a relevant access or technical-support question.

## 5. Same facts, different foreground

Audience tailoring changes the order and depth of explanation, not the result.

| Decision-maker | Technical reviewer |
| --- | --- |
| Lead with the conclusion, implication, and proposed action | Explain definitions, data, method, evaluation, and limitations |
| Use direct language and selected evidence | Provide reproducible detail and diagnostic evidence |
| State caveats that could change the decision | Make assumptions and uncertainty assessable |
| Offer deeper detail as needed | Connect technical findings to the substantive question |

These are defaults, not stereotypes. An executive may need methods to assess risk, and an analyst still benefits from a clear conclusion.

A material data correction must be disclosed to both audiences. Putting it in an appendix is not sufficient if it changes the recommendation.

### Interpret the 82% precision example correctly

Precision is the proportion of flagged cases that are actually positive under the evaluation's definition:

```text
Precision = true positives / (true positives + false positives)
```

The supplied 82% is a hypothetical model result, not evidence from this repository. It is not accuracy, recall, a guarantee for each individual, or proof that tutoring will improve completion.

Funding also depends on issues such as the number of flags, missed cases, evaluation design, support capacity, costs, and intervention effectiveness. A feature that may fail to generalise next term is a decision-relevant caveat for both audiences.

See [scikit-learn's precision definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html).

## 6. Worked practice

### Practice 1 — Classify the activity

| Activity | Type | Why |
| --- | --- | --- |
| Twenty quick histograms of new data | Exploratory | Used to discover the data's structure |
| One annotated chart in a board presentation | Explanatory | Selected evidence for an audience |
| A rough scatter plot checking a hunch | Exploratory | Investigates a question |
| A polished figure explaining a published result | Explanatory | Communicates a finding with context |

The colleague who pastes all twenty histograms into a client deck makes the client perform the analyst's selection work. Choose the visuals necessary for the conclusion, polish them, explain what each contributes, and retain other evidence in supporting material.

The healthy practice is selective communication, not following a literal hundred-to-one ratio.

### Practice 2 — Structure the late-enrolment story

**Setup:** We want students to complete the portal course and need to understand whether enrolment timing is associated with completion before the deadline.

**Conflict:** In the exercise's hypothetical finding, students enrolling in the final week have lower completion. Show cohort completion rates with group sizes, dates, and a clearly defined denominator.

**Resolution:** First check whether late enrollees simply had less time and whether cohort characteristics differ. If the finding remains relevant, pilot additional onboarding or a targeted support option and evaluate the outcome.

A sweeping late-enrolment ban is not justified by this association alone. Compare equal follow-up windows when answering engagement questions, while retaining the deadline-based outcome if the decision specifically concerns deadline completion.

Without narrative, the audience may ask: “What explains the difference, and what should we change?”

The story links a supported observation to an action proportionate to the evidence.

### Practice 3 — A teacher-admin dashboard

The recurring questions are:

1. Who is waiting for approval?
2. Who is behind the required schedule and needs review?
3. Which lessons are producing completion bottlenecks?
4. How is progress changing over time and across comparable cohorts?

Use pending approvals as the leading metric for this proposed workflow. If support prioritisation becomes the primary responsibility, a different first view may be more appropriate.

Include five views in priority order:

| Priority | View | Decision supported |
| --- | --- | --- |
| 1 | Pending-approval count and queue link | Review applications |
| 2 | Behind-schedule worklist | Investigate who needs support |
| 3 | Lesson non-completion bars with counts and denominators | Review possible lesson bottlenecks |
| 4 | Weekly completion-event line | Inspect activity changes |
| 5 | Comparable cohort completion rates | Investigate group differences |

Exclude a decorative 3-D browser-share pie, repetitive minor-event sparklines, and a broad lifetime visitor total because they do not answer these recurring decisions.

The [dashboard design brief](./lesson03-dashboard-design.md) defines proposed metrics, scope, refresh behaviour, exclusions, and review checks. It is a design exercise, not a connected dashboard.

### Practice 4 — Retell the same model finding

**A. For the dean**

“The model achieved 82% precision in the evaluation, so its flags may help prioritise a tutoring pilot. A last-login feature may not carry over to next term, and precision alone does not establish the programme's impact or cost effectiveness. Consider a capacity-limited pilot with next-term validation before committing to a wider rollout.”

**B. For a fellow data scientist**

“The reported evaluation precision is 0.82 for the stated positive class and threshold; the prompt does not provide sample size, recall, uncertainty, or the validation split. Last-login recency may shift next term, so assess prediction-time availability and temporal generalisation. Report the additional metrics and evaluate any tutoring intervention separately from the model's classification performance.”

Both versions retain 82% precision and the generalisation concern. The dean's version foregrounds a funding decision; the analyst's version foregrounds what must be checked to assess the evaluation.

Neither claims that the model is automatically reliable enough to fund or that intervention success follows from prediction performance.

### Practice 5 — An analysis-to-action playbook

1. **Define the audience and decision.** State what the recipient needs to understand or decide.
2. **Select explanatory evidence.** Keep the few visuals needed for the finding, with methods and other checks available.
3. **Build the narrative.** Provide setup, important finding, limitations, and a proportionate recommendation.
4. **Choose the product.** Use a story for a specific investigation and a dashboard for recurring monitoring.
5. **Tailor depth and check honesty.** Verify axes, units, comparison windows, denominators, uncertainty, and material caveats.
6. **Specify follow-up.** Identify an owner, next action, and the outcome or evidence that will inform the next review.

**Closing principle:** analysis becomes useful when its evidence and limits are communicated clearly enough to support a justified decision.

A valuable decision can be to investigate further or avoid an unsupported action; not every insight needs immediate operational change.

## 7. Theory exercises — suggested answers

Use these as study references and explain the ideas in your own words for course submissions.

### Task 1 — Exploratory versus explanatory visuals

Exploratory visualisation is mainly for analysts investigating data. Its goal is to discover patterns, anomalies, and useful questions, often through many provisional plots.

Explanatory visualisation is for an audience that needs to understand a finding or make a decision. It uses a selected set of readable charts with enough context to communicate what matters.

Both need honest data and meaningful scales; they differ chiefly in purpose and audience.

### Task 2 — Shipping-cost story

**Setup:** The company needs to understand why shipping costs have risen and decide how to control them without damaging delivery service. Define the comparison period, shipment population, and cost measure.

**Conflict:** In the scenario, costs have increased by 20%, and the analysis attributes the increase to a specific regional carrier. Show the overall change and a carrier-level breakdown, explaining whether the metric is total spend or a like-for-like cost per shipment.

**Resolution:** Review the carrier's rates and service performance, then assess renegotiation or a controlled reallocation of shipments. State the decision owner and monitor both costs and delivery outcomes after any change.

The narrative connects the finding to a practical response rather than displaying an unexplained cost chart.

### Task 3 — Dashboard design principles

An everything dashboard shows too many charts simply because data is available. Important signals become difficult to find, and users must guess which panels matter.

Avoid it by starting with the audience's recurring questions and decisions. Define the relevant metrics, choose a small prioritised set of views, make scope and freshness clear, and remove redundant or irrelevant panels. Test whether users can identify what requires attention.

### Task 4 — Communicate a data correction

For an executive, explain the corrected conclusion first, what changed, and whether the decision or recommendation needs revision. Disclose the error and its material effect directly, then offer technical detail as needed.

For a fellow analyst, also provide the source of the error, affected records or calculations, the correction, before-and-after results, and the checks used to verify the revision.

Both audiences receive the same corrected facts and important limitations. Only the order and technical depth differ.

### Task 5 — From EDA to communication

EDA charts record an investigation: they may include tentative hypotheses, repeated views, and plots that turned out not to matter. A decision-making audience generally needs selected evidence, its meaning, and the justified next step.

Presenting the entire exploratory set makes the audience repeat the analyst's interpretation work and can hide the main finding. Choose the necessary explanatory charts, add context and caveats, and keep the remaining work available as supporting material.

## 8. Module revision checklist

- [ ] Choose visual channels and chart types for the intended question.
- [ ] Keep axes, units, scales, and selections honest.
- [ ] Select explanatory charts rather than exporting every EDA plot.
- [ ] Connect context, finding, and recommendation.
- [ ] Define dashboard metrics, denominators, filters, and refresh times.
- [ ] Make the most important recurring decision easy to identify.
- [ ] Tailor detail while preserving material facts and caveats.
- [ ] Separate predictive performance from intervention effectiveness.
- [ ] Give the audience a justified next step and a way to evaluate it.

## Sources

- User-supplied course material: *Module VII: Data Visualization, Dashboards and Storytelling with Data*.
- [Tableau: Best Practices for Effective Dashboards](https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm) — audience, purpose, and prioritised views.
- [scikit-learn: precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html) — precision definition.

Worked responses, clarifying notes, and the dashboard design brief were prepared for this repository.

[Previous lesson](./Lesson-02-Choosing-the-Right-Plot-and-Tools.md) · [Module overview](./README.md) · [Theory index](../README.md)
