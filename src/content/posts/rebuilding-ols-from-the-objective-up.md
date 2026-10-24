---
title: "Rebuilding OLS from the objective up"
summary: "Start with the squared-error objective, derive the normal equation, then solve the problem without explicitly inverting a matrix."
date: 2026-10-24
draft: false
featured: true
tags:
  - linear algebra
  - machine learning
  - from scratch
thumbnail: "/images/posts/ols-fit.svg"
thumbnailAlt: "A set of observations around an oxblood least-squares regression line on a quiet coordinate grid."
artifactSummary: "A small NumPy estimator that fits an intercept and coefficients with a least-squares solver. The complete source is available as a standalone file."
artifactUrl: "/code/ols.py"
caption: "A conceptual view of a fitted line and its residuals, included to orient the reader rather than claim a benchmark result."
---

Linear regression is often introduced as a formula and then hidden behind a single library call. I wanted to work through the part between those two things: what objective are we minimizing, how does the solution follow from it, and what does a small implementation need to get right?

This is an educational baseline, not a drop-in replacement for scikit-learn. It handles dense, finite, two-dimensional feature matrices and a one-dimensional target. It deliberately leaves out sample weights, sparse inputs, multi-output regression, statistical inference, and the rest of a production estimator's interface.

## The objective

Given a design matrix \(X\), target vector \(y\), and coefficient vector \(\beta\), ordinary least squares chooses the coefficients that minimize the sum of squared residuals:

$$
\hat{\beta} = \arg\min_{\beta} \|y - X\beta\|_2^2
$$

For a model with an intercept, the simplest representation is to prepend a column of ones to \(X\). The intercept then becomes the first coefficient, so the same least-squares objective handles both the offset and the feature weights.

Let the objective be \(J(\beta) = (y-X\beta)^T(y-X\beta)\). Expanding the expression gives:

$$
J(\beta) = y^Ty - 2\beta^TX^Ty + \beta^TX^TX\beta
$$

Taking the gradient with respect to \(\beta\):

$$
\nabla_\beta J = -2X^Ty + 2X^TX\beta
$$

At a stationary point, the gradient is zero. That gives the normal equation:

$$
X^TX\hat{\beta}=X^Ty
$$

When the columns of \(X\) are linearly independent, the coefficient vector is unique and can be written as:

$$
\hat{\beta}=(X^TX)^{-1}X^Ty
$$

That expression is useful for understanding the solution. It does not mean that explicitly computing the inverse is the best implementation strategy.

## The implementation

The implementation in this repository calls [NumPy’s `linalg.lstsq`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html) on the design matrix directly. It avoids forming the inverse of \(X^TX\), exposes the fitted coefficients and intercept, and records the rank and singular values returned by the solver.

The core operation is small:

```python
solution, residuals, rank, singular_values = np.linalg.lstsq(
    design, y_array, rcond=None
)
```

The rest is mostly contract enforcement: check dimensions, verify that the number of rows matches the number of targets, reject non-finite values, and make sure `predict` receives the same number of features seen during fitting.

A small class is useful here because it makes the fitted state explicit. The model stores `coef_`, `intercept_`, `n_features_in_`, `rank_`, `singular_values_`, and the residual sum of squares. These names are familiar to people who have used estimator APIs, but the class does not claim API compatibility with scikit-learn.

## What the tests establish

The tests use a synthetic target with a known linear relationship. The fitted intercept and coefficients are checked against the known values, and predictions are checked against the target. There are also tests for a model without an intercept, inconsistent input shapes, non-finite values, prediction before fitting, and a rank-deficient design matrix.

Run the tests from the project root after installing NumPy:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

These tests establish behavior for the cases they cover. They do not establish parity with scikit-learn, performance superiority, or robustness across every numerical regime. A broader comparison would need a fixed experiment matrix, carefully chosen tolerances, and explicit treatment of rank and conditioning.

## What broke / where it can diverge

### The inverse is a derivation, not an instruction

Explicitly computing \((X^TX)^{-1}\) can amplify numerical error. Forming \(X^TX\) also squares the condition number of the design matrix in the usual 2-norm setting. A direct least-squares solver is a better default for the implementation, while the normal equation remains a useful derivation of the optimum.

### Rank deficiency changes what can be identified

If one feature is an exact linear combination of another, there is no unique coefficient vector. The predictions may still be well-defined over the observed design space, even though multiple coefficient vectors minimize the same objective. The implementation records the rank reported by the solver so that this situation is visible rather than silently treating every fit as full-rank.

### Good fit does not imply a good model

OLS minimizes squared residuals on the supplied observations. It does not guarantee that the relationship generalizes, that the errors satisfy a statistical model, or that a coefficient has a causal interpretation. Those are separate questions and need separate assumptions and diagnostics.

### The interface is intentionally incomplete

This implementation does not yet support sparse matrices, sample weights, multiple target columns, missing-value handling, or the broader estimator conventions of scikit-learn. Matching one small synthetic case is not enough to call it a drop-in replacement. That claim would require parity tests across documented behavior and edge cases.

## What I would test next

The next useful experiment is a reproducible comparison against [`sklearn.linear_model.LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) across well-conditioned, nearly collinear, and rank-deficient inputs. I would record prediction error, coefficient differences where coefficients are identifiable, runtime, and behavior as feature scales diverge. Results should be saved with the test setup and tolerance choices, not reduced to one “matches” number.

The point of rebuilding a familiar algorithm is not to produce another formula-shaped class. It is to make the assumptions and numerical choices visible enough that the boundaries of the implementation can be tested.
