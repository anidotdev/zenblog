"""A deliberately small ordinary least-squares estimator.

This implementation is an educational baseline, not a drop-in replacement
for scikit-learn. It accepts a dense, finite, two-dimensional feature matrix
and a one-dimensional target vector.
"""

from __future__ import annotations

import numpy as np


class LinearRegressionOLS:
    """Fit a linear model by minimizing the sum of squared residuals."""

    def __init__(self, fit_intercept: bool = True) -> None:
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float | None = None
        self.n_features_in_: int | None = None
        self.rank_: int | None = None
        self.singular_values_: np.ndarray | None = None
        self.residual_sum_squares_: float | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegressionOLS":
        X_array = np.asarray(X, dtype=np.float64)
        y_array = np.asarray(y, dtype=np.float64)

        if X_array.ndim != 2:
            raise ValueError("X must be a 2D feature matrix.")
        if y_array.ndim != 1:
            raise ValueError("y must be a 1D target vector.")
        if X_array.shape[0] == 0:
            raise ValueError("X must contain at least one observation.")
        if X_array.shape[0] != y_array.shape[0]:
            raise ValueError("X and y must contain the same number of observations.")
        if X_array.shape[1] == 0:
            raise ValueError("X must contain at least one feature.")
        if not np.isfinite(X_array).all() or not np.isfinite(y_array).all():
            raise ValueError("X and y must contain only finite values.")

        self.n_features_in_ = int(X_array.shape[1])
        design = (
            np.column_stack((np.ones(X_array.shape[0]), X_array))
            if self.fit_intercept
            else X_array
        )

        # Solve the least-squares problem directly. Do not explicitly compute
        # (X.T @ X)^-1: forming and inverting that matrix can worsen numerical
        # error, especially when feature columns are poorly conditioned.
        solution, _residuals, rank, singular_values = np.linalg.lstsq(
            design, y_array, rcond=None
        )

        if self.fit_intercept:
            self.intercept_ = float(solution[0])
            self.coef_ = solution[1:].copy()
        else:
            self.intercept_ = 0.0
            self.coef_ = solution.copy()

        prediction = design @ solution
        self.residual_sum_squares_ = float(np.sum((y_array - prediction) ** 2))
        self.rank_ = int(rank)
        self.singular_values_ = singular_values.copy()
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None or self.intercept_ is None or self.n_features_in_ is None:
            raise RuntimeError("Call fit(X, y) before predict(X).")

        X_array = np.asarray(X, dtype=np.float64)
        if X_array.ndim != 2:
            raise ValueError("X must be a 2D feature matrix.")
        if X_array.shape[1] != self.n_features_in_:
            raise ValueError(
                f"X must contain {self.n_features_in_} feature(s); "
                f"received {X_array.shape[1]}."
            )
        if not np.isfinite(X_array).all():
            raise ValueError("X must contain only finite values.")

        return X_array @ self.coef_ + self.intercept_
