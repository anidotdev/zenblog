import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "ols"))
from ols import LinearRegressionOLS  # noqa: E402


class LinearRegressionOLSTests(unittest.TestCase):
    def test_recovers_exact_linear_relationship(self):
        X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 3.0]])
        y = 3.0 + 2.0 * X[:, 0] - 4.0 * X[:, 1]

        model = LinearRegressionOLS().fit(X, y)

        np.testing.assert_allclose(model.intercept_, 3.0, atol=1e-12)
        np.testing.assert_allclose(model.coef_, [2.0, -4.0], atol=1e-12)
        np.testing.assert_allclose(model.predict(X), y, atol=1e-12)
        self.assertAlmostEqual(model.residual_sum_squares_, 0.0, places=20)

    def test_no_intercept_mode(self):
        X = np.arange(1.0, 6.0).reshape(-1, 1)
        y = 2.5 * X[:, 0]

        model = LinearRegressionOLS(fit_intercept=False).fit(X, y)

        self.assertEqual(model.intercept_, 0.0)
        np.testing.assert_allclose(model.coef_, [2.5], atol=1e-12)

    def test_rank_deficient_matrix_still_predicts_least_squares_solution(self):
        base = np.arange(1.0, 6.0)
        X = np.column_stack((base, 2.0 * base))
        y = 5.0 + 3.0 * base

        model = LinearRegressionOLS().fit(X, y)

        self.assertLess(model.rank_, X.shape[1] + 1)
        np.testing.assert_allclose(model.predict(X), y, atol=1e-11)

    def test_rejects_inconsistent_lengths(self):
        with self.assertRaisesRegex(ValueError, "same number of observations"):
            LinearRegressionOLS().fit(np.ones((3, 2)), np.ones(2))

    def test_rejects_nan_values(self):
        with self.assertRaisesRegex(ValueError, "finite values"):
            LinearRegressionOLS().fit(np.array([[1.0], [np.nan]]), np.array([1.0, 2.0]))

    def test_predict_requires_a_fitted_model(self):
        with self.assertRaisesRegex(RuntimeError, "Call fit"):
            LinearRegressionOLS().predict(np.ones((2, 1)))

    def test_predict_checks_feature_count(self):
        model = LinearRegressionOLS().fit(np.arange(5.0).reshape(-1, 1), np.arange(5.0))
        with self.assertRaisesRegex(ValueError, "feature"):
            model.predict(np.ones((2, 2)))

    def test_public_artifact_is_synced_with_canonical_source(self):
        canonical = ROOT / "examples" / "ols" / "ols.py"
        public_copy = ROOT / "public" / "code" / "ols.py"
        self.assertEqual(canonical.read_text(encoding="utf-8"), public_copy.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
