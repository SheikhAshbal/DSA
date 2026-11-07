# Lesson 3: Feature Extraction, Encoding and Scaling

[Theory index](../README.md) · [Module overview](./README.md) · [Previous lesson](./Lesson-02-Cleaning-Missing-Values-Duplicates-Formats-and-Text.md)

**Course:** Data Science and Analytics  
**Module III:** Data Wrangling and Preprocessing  
**Estimated study time:** 55 minutes

## Learning objectives

- Extract informative features from raw fields.
- Choose encodings appropriate to ordered and unordered categories.
- Explain standardisation and min-max scaling.
- Keep test information out of fitted preprocessing.
- Assemble a reproducible preprocessing workflow.

## 1. Feature extraction: expose useful signals

Feature extraction derives variables that make a useful pattern more explicit. Cleaning makes a timestamp valid; feature extraction turns it into an hour, a night-time indicator, or an elapsed-time measurement.

For suspicious-login detection, a raw timestamp such as `2026-08-29 03:14:07` contains a time-of-day signal. Extracting `hour = 3` or `is_night = True` makes that signal easier for a model to use. Define “night” explicitly and use a suitable timezone.

| Feature | Inputs needed | Signal exposed |
| --- | --- | --- |
| hour / is_night | Current login timestamp and timezone | Access outside expected hours |
| seconds_since_last_login | Current and previous login timestamps | Unusually short gaps or rapid activity |
| is_new_ip | Current IP and the account's prior IP history | First use of an address by this account |
| country | IP plus a geolocation lookup | Geographic context |
| is_new_device | Parsed user-agent or a device identifier plus prior account history | A device not previously observed |

These signals are evidence for a model, not proof of compromise. Night work, travel, shared networks, and browser changes can produce legitimate unusual activity.

**Input limitations:** an IP string alone does not reveal whether it is new to a user. A user-agent string is not a reliable unique physical-device identifier. Impossible-travel detection requires location changes and elapsed time; a short gap alone does not establish impossible travel.

Historical features must use only information available before the login being evaluated. Looking at later events would leak future information.

## 2. Encoding categorical features

Many models need numeric representations of categories. The representation should match the meaning of the variable.

### Ordered categories: ordinal integer codes

For `low < medium < high`, a mapping such as `low=0, medium=1, high=2` preserves the order.

The course calls this **label encoding**. For input features, **ordinal encoding** is the more precise term. In scikit-learn, use an appropriate feature encoder with explicit category order rather than assuming alphabetic order reflects meaning.

Integer spacing is still an assumption: the difference between low and medium is not necessarily quantitatively equal to the difference between medium and high.

### Unordered categories: one-hot encoding

Colours and payment methods have no inherent rank. Mapping red=0, green=1, blue=2 can introduce artificial order and distances in models that interpret those numbers arithmetically.

One-hot encoding creates binary indicator columns:

| Colour | colour_red | colour_green | colour_blue |
| --- | ---: | ---: | ---: |
| Red | 1 | 0 | 0 |
| Green | 0 | 1 | 0 |
| Blue | 0 | 0 | 1 |

It avoids an arbitrary numeric ranking. A downside is increased dimensionality: a 50-category field can produce 50 columns in the full representation. Choose a strategy for unseen categories and keep the train/test column schema consistent.

Not every algorithm treats integer codes identically; the lesson's warning applies when numeric codes impose unintended ordering or distances. Some models support categorical inputs directly.

## 3. Scaling numeric features

Age might vary by tens of years while income varies by hundreds of thousands of currency units. In raw Euclidean distances, the larger numeric differences can overwhelm smaller ones.

Scaling changes the units so that raw magnitude is less likely to determine the result. It does not guarantee equal predictive importance or remove outliers.

### Standardisation

For a nonconstant feature:

```text
z = (x - training_mean) / training_standard_deviation
```

The fitted training feature has mean 0 and standard deviation 1, apart from numerical precision. There is no fixed output range, and the distribution does not become normally distributed merely because it was standardised.

### Min-max scaling

For a nonconstant feature and target range [0, 1]:

```text
scaled_x = (x - training_minimum) / (training_maximum - training_minimum)
```

The fitted training minimum becomes 0 and maximum becomes 1. A new test value outside the training range can map below 0 or above 1 unless clipping is explicitly used.

| Property | Standardisation | Min-max scaling |
| --- | --- | --- |
| Reference quantities | Mean and standard deviation | Minimum and maximum |
| Training result | Mean 0, standard deviation 1 | Values between 0 and 1 |
| Fixed output bounds | No | For training values; unseen values may exceed them |
| Sensitive to extreme observations | Yes | Yes |

Handle constant features explicitly because their standard deviation and range are zero.

### Which models need attention to scale?

- Distance-based methods such as k-nearest neighbours and k-means are sensitive to feature units.
- Many gradient-based and regularised models benefit from scaling through better numerical conditioning or comparable penalty effects.
- Ordinary decision trees and tree ensembles generally do not require scaling: splits depend on ordering and thresholds, which positive affine rescaling preserves. Numerical and implementation details can still produce small differences.

## 4. The leakage trap: learn from training data only

If the mean and standard deviation are calculated using the entire dataset, test observations influence the transformation used during training. The test set is no longer fully held out.

The evaluation can become overly optimistic and is no longer a clean estimate of performance on unseen data. Leakage does not guarantee that every measured score increases; the methodological error exists even if the score barely changes.

```text
Separate train and test
          |
          v
Fit preprocessing on training data
          |
          +--> Transform training data --> Train model
          |
          +--> Transform test data -----> Evaluate once
```

Use the same fitted parameters for both partitions. Fitting a second scaler on the test set gives a different coordinate system and also violates the held-out evaluation procedure.

**Important clarification to the course sequence:** the rule extends to learned imputation, category vocabularies, and feature selection. Fixed row-wise rules such as trimming whitespace or extracting an hour can be applied consistently without learning test statistics. Fit data-dependent operations only after the split. For cross-validation, fit them within each training fold. See the [scikit-learn guidance on leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).

## 5. Worked practice

### Practice 1 — Extract suspicious-login features

For `login_timestamp`, extract hour and a night-time indicator to expose odd-hour access. From the current and previous login timestamps, calculate elapsed seconds to expose rapid activity. From the IP and prior account history, derive whether the address is new; use an external lookup for country. From a parsed user-agent or device identifier and past history, derive a new-device indicator.

The raw fields in the prompt do not supply every required historical or lookup input. State those dependencies rather than pretending the extra features can be derived from a single string.

An `is_night` feature can help because it expresses the relevant time pattern directly instead of requiring the model to discover it from a raw timestamp.

### Practice 2 — Match encodings to meaning

| Field | Course choice | Justification |
| --- | --- | --- |
| risk_level: low / medium / high | Label / ordinal | A meaningful order exists |
| country: 50 values | One-hot | No inherent numerical rank |
| t_shirt_size: S / M / L / XL | Label / ordinal | Sizes have a meaningful order |
| payment_method: card / cash / transfer | One-hot | Methods have no inherent rank |

Coding countries as 0–49 can suggest that country 49 is larger than country 0 or that code differences measure similarity. Those relationships are invented.

One-hot encoding a 50-value country field can add 50 columns. The memory and dimensionality cost matters as the number of categories and records grows.

### Practice 3 — Compare raw and standardised values

This standalone demonstration uses Python's standard library. It illustrates scaling on one toy sample, not a model-evaluation workflow.

```python
import statistics as st

age = [20, 22, 25, 30, 45]
income = [30000, 32000, 50000, 80000, 250000]

def standardise(values):
    mean = st.mean(values)
    std = st.pstdev(values)
    if std == 0:
        return [0.0 for _ in values]
    return [round((value - mean) / std, 2) for value in values]

print("age raw range:", max(age) - min(age))
print("income raw range:", max(income) - min(income))
print("age z:", standardise(age))
print("income z:", standardise(income))
```

Expected output:

```text
age raw range: 25
income raw range: 220000
age z: [-0.94, -0.71, -0.38, 0.18, 1.85]
income z: [-0.71, -0.68, -0.46, -0.1, 1.95]
```

Before scaling, income's numeric range is much larger. Afterwards, both features are expressed in standard-deviation units. Standardisation does not force their ranges to be identical. Round for display, not before real model training.

k-NN and k-means use distances that depend on units, while a decision tree usually selects equivalent splits after positive affine rescaling.

### Practice 4 — Explain scaling leakage

1. **What leaked?** The held-out observations influenced the mean and standard deviation applied during training.
2. **Why is evaluation compromised?** The preparation process used information from data intended to represent unseen cases. The score may therefore be overly optimistic.
3. **Correct sequence:** split first, fit the scaler using training observations, then transform both training and test observations using that fitted scaler.
4. **Why can accuracy alone miss it?** A score does not reveal how the preprocessing parameters were obtained. A plausible score is not evidence of a valid evaluation procedure.

The general rule is: learn preprocessing parameters from training data and apply the unchanged rules to held-out data.

### Practice 5 — Assemble the full recipe

The course's abbreviated order is:

```text
Assess -> Clean -> Extract -> Encode -> Split -> Scale
```

This is safe only when the steps before splitting use fixed rules and no information learned from the held-out observations. Cleaning can include a median imputation, and encoding can learn a category vocabulary, so they are not automatically safe before splitting.

A more general recipe is:

1. Define the prediction target, available information, and evaluation design.
2. Preserve raw input, assess schema issues, and define fixed validation rules.
3. Resolve accidental copies and grouping constraints so related records do not improperly cross partitions.
4. Split into train/test using an appropriate random, grouped, or chronological design.
5. Apply fixed cleaning and feature-extraction rules consistently; historical features must respect event time.
6. Fit learned cleaning rules, encoders, and scalers using training data only.
7. Transform train and test with the same fitted preprocessing.
8. Train and evaluate the model; verify schema, missingness, and unseen-category handling.

A fitted pipeline helps keep these dependencies together. Learning an imputation median before the split can leak information just as fitting a scaler before the split can.

## 6. Theory exercises — suggested answers

Use these as study references and explain the reasoning in your own words for course submissions.

### Task 1 — Feature extraction purpose

Feature extraction creates variables that make useful patterns easier for a model to learn. For example, a raw login timestamp contains the hour, but it does not explicitly say whether the login happened at night. Extracting the hour or creating an `is_night` indicator exposes that pattern directly and can help a suspicious-login model identify unusual access times. Its usefulness depends on the user's normal activity and the chosen timezone.

### Task 2 — Choosing the correct encoding

For Customer Tier, use label encoding in the course's terminology, more precisely ordinal encoding for an input feature. Bronze, Silver, and Gold have a meaningful ranking, so an explicit Bronze=0, Silver=1, Gold=2 mapping preserves it.

For Favorite Color, use one-hot encoding. Red, Blue, and Green have no natural order. Separate binary columns avoid suggesting that one colour is numerically greater than another. Tier codes still should not be interpreted as measured equal distances between benefits.

### Task 3 — The necessity of scaling

With features such as age and income, the larger numeric differences in income can dominate distance calculations even when income is not more informative. Scaling makes the numeric magnitudes more comparable and can also help the optimisation and regularisation of scale-sensitive models.

Ordinary tree-based models are the main exception in this lesson. They split features using ordered thresholds, so positive affine rescaling generally preserves the possible partitions and scaling is usually unnecessary.

### Task 4 — Comparing scaling methods

Standardisation subtracts a feature's training mean and divides by its training standard deviation. The fitted nonconstant training feature has mean 0 and standard deviation 1. Its values are not limited to a fixed range, and this operation does not make the distribution normal.

Min-max scaling uses the training minimum and maximum to map training values into a chosen range, usually 0–1. It sets bounds for the fitted training sample rather than a target mean and standard deviation. Unseen values outside the original range can transform outside 0–1.

### Task 5 — Analysing the leakage trap

Calculating scaling parameters from the full dataset lets the test set influence preprocessing used for training. This is data leakage because the test set should represent information unavailable when building the model.

It undermines the independence of the final evaluation and can produce overly optimistic performance estimates. The size or direction of the numerical change is not guaranteed, but the evaluation procedure is compromised.

The correct approach is to split first, calculate the mean and standard deviation from training data only, and use those same values to transform both training and test data.

## 7. Module revision checklist

- [ ] Assess before making changes and keep raw input unchanged.
- [ ] Choose missing-data policies based on evidence and purpose.
- [ ] Distinguish accidental duplicates from legitimate repeated observations.
- [ ] Normalise field formats and validate extracted values.
- [ ] Derive features using information available at prediction time.
- [ ] Preserve real category order without inventing nominal rankings.
- [ ] Choose scaling appropriate to the model.
- [ ] Split before fitting any data-dependent preprocessing.
- [ ] Fit within each training fold during cross-validation.
- [ ] Record decisions and reproduce the final dataset from code.

## Sources

- User-supplied course material: *Data Science and Analytics, Module III: Data Wrangling and Preprocessing, Feature Extraction, Encoding and Scaling*.
- [scikit-learn: Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html) — clarification of train-only fitting and leakage.
- [scikit-learn: Preprocessing data](https://scikit-learn.org/stable/modules/preprocessing.html) — reference for encodings and scaling behaviour.

Worked responses and clarifying notes were prepared for this repository.

[Previous lesson](./Lesson-02-Cleaning-Missing-Values-Duplicates-Formats-and-Text.md) · [Module overview](./README.md) · [Theory index](../README.md)
