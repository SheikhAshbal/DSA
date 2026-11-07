# Teacher-Admin Dashboard: Design Brief

[Lesson 3](./Lesson-03-Dashboards-and-Storytelling-with-Data.md) · [Module overview](./README.md)

**Purpose:** help a teacher-admin manage approvals, identify students needing review, find lesson bottlenecks, and monitor progress.

This is a proposed design based on the course scenario. It contains no measured portal results, deployed dashboard, or live data connection.

## Audience and recurring decisions

| Question | Decision the dashboard supports |
| --- | --- |
| Which applications need attention? | Review the approval queue |
| Which students are behind the required schedule? | Inspect context and prioritise support |
| Which lessons have unusually high non-completion? | Review content, access, and assessment issues |
| Is activity changing over the term? | Investigate cohorts, scheduling, and recording changes |

## Reading order and five panels

| Priority | Panel | Metric or content | User action |
| --- | --- | --- | --- |
| 1 | Pending approvals card | Distinct application IDs currently in pending status, within the selected course/batch scope | Open approval worklist |
| 2 | Behind-schedule worklist | Students with at least one required lesson due and fewer completed due lessons than due lessons | Review individual circumstances before contacting |
| 3 | Lesson bottleneck bars | Incomplete due student–lesson pairs divided by all due student–lesson pairs for each lesson; display numerator and denominator | Inspect lesson details |
| 4 | Weekly completions line | Distinct student–lesson completions first recorded in each displayed week | Investigate activity changes |
| 5 | Cohort completion comparison | Completion rate for cohorts with the same defined follow-up window; show cohort sizes and exclusions | Compare like-for-like cohorts |

Place the leading metric prominently for the intended reading direction and device. On a small screen, preserve this priority order rather than shrinking every panel until it is unreadable.

Five panels satisfy the course exercise; a production design might combine panels or split them into a second view after user testing.

## Definitions to agree before implementation

- **Snapshot:** a stated date and time used consistently for status, due dates, and completions.
- **Scope:** selected course and batch; make filter coverage explicit on every panel.
- **Student identity:** stable ID, not display name.
- **Application identity:** stable application ID; reapplications need a stated counting rule.
- **Due lesson:** a required, assigned lesson whose due time is at or before the snapshot.
- **Completed due lesson:** a due lesson with a valid completion event at or before the snapshot.
- **Weekly completion:** first valid completion per student–lesson pair, assigned to a week in the stated timezone.
- **Cohort rate:** students meeting the defined completion outcome within a fixed follow-up window divided by eligible students with that full window observed.
- **Zero denominator:** display “not applicable” with the reason rather than a zero percent.
- **Missing records:** show as unknown or a data-quality issue, not automatically as non-completion.

A behind-schedule rule is a descriptive worklist criterion, not a validated predictive model or proof of disengagement.

## Refresh and data status

Choose refresh frequency according to how often the teacher acts. A proposed daily snapshot may be sufficient for progress review, while approval operations may need a fresher status check.

Show:

- Data-as-of timestamp and timezone.
- Last successful refresh.
- Any stale-data or failed-refresh warning.
- Active course/batch filters and displayed date range.
- Metric definitions and denominators through visible notes or detail views.

A chart refresh does not itself update every operational system. Recheck an application's current status before making an approval decision.

## Deliberate exclusions

| Excluded panel | Reason |
| --- | --- |
| Decorative 3-D browser-share pie | Does not support the stated teaching decisions |
| Twelve similar sparklines for minor events | Repetition distracts from higher-priority questions |
| Lifetime all-portal visitor total | A broad activity count is not a direct measure of current student progress |

Browser information can become relevant if access problems are being investigated; keep that in a diagnostic view rather than permanently occupying the main dashboard.

## Review checklist

- [ ] Each panel answers a named decision.
- [ ] Rates have explicit denominators and comparable follow-up.
- [ ] Counts deduplicate the intended event or entity.
- [ ] Current-state metrics and time-window metrics are distinguished.
- [ ] Filters affect panels as labelled.
- [ ] Unknown, stale, and zero states look different.
- [ ] Charts have readable labels, units, and suitable scales.
- [ ] Support worklists display only the information needed by authorised users.
- [ ] The teacher can identify a next action without guessing what the metric means.

## From monitoring to a one-off story

If the dashboard surfaces lower completion among late enrollees, investigate exposure time, cohort composition, and recording quality first. Then create a short explanatory story for the specific decision, with selected evidence and a proportionate recommendation.

[Back to Lesson 3](./Lesson-03-Dashboards-and-Storytelling-with-Data.md)
