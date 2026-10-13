"""
Unit Tests for AI Model Evaluation Metrics Module
"""

import pytest
import numpy as np
from src.metrics import (
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error,
    evaluate_model_performance,
    EvaluationError
)


def test_perfect_predictions():
    y_true = [1.0, 2.0, 3.0, 4.0]
    y_pred = [1.0, 2.0, 3.0, 4.0]

    assert mean_squared_error(y_true, y_pred) == pytest.approx(0.0)
    assert root_mean_squared_error(y_true, y_pred) == pytest.approx(0.0)
    assert mean_absolute_error(y_true, y_pred) == pytest.approx(0.0)
    assert r2_score(y_true, y_pred) == pytest.approx(1.0)
    assert mean_absolute_percentage_error(y_true, y_pred) == pytest.approx(0.0)


def test_known_values():
    y_true = [3.0, -0.5, 2.0, 7.0]
    y_pred = [2.5, 0.0, 2.0, 8.0]

    # Differences: [-0.5, 0.5, 0.0, 1.0] -> Abs: [0.5, 0.5, 0.0, 1.0] -> MAE = 2.0 / 4 = 0.5
    assert mean_absolute_error(y_true, y_pred) == pytest.approx(0.5)

    # Squared differences: [0.25, 0.25, 0.0, 1.0] -> MSE = 1.5 / 4 = 0.375
    assert mean_squared_error(y_true, y_pred) == pytest.approx(0.375)
    assert root_mean_squared_error(y_true, y_pred) == pytest.approx(np.sqrt(0.375))


def test_shape_mismatch_raises_evaluation_error():
    y_true = [1.0, 2.0, 3.0]
    y_pred = [1.0, 2.0]

    with pytest.raises(EvaluationError, match="Shape mismatch"):
        mean_squared_error(y_true, y_pred)


def test_empty_array_raises_evaluation_error():
    with pytest.raises(EvaluationError, match="must not be empty"):
        mean_absolute_error([], [])


def test_nan_values_raise_evaluation_error():
    y_true = [1.0, np.nan, 3.0]
    y_pred = [1.0, 2.0, 3.0]

    with pytest.raises(EvaluationError, match="Inputs contain NaN"):
        r2_score(y_true, y_pred)


def test_zero_variance_r2_handling():
    # True target is constant (zero total sum of squares)
    y_true = [5.0, 5.0, 5.0]
    y_pred_perfect = [5.0, 5.0, 5.0]
    y_pred_off = [4.0, 6.0, 5.0]

    assert r2_score(y_true, y_pred_perfect) == 1.0
    assert r2_score(y_true, y_pred_off) == 0.0


def test_evaluate_model_performance_report_structure():
    y_true = [10.0, 20.0, 30.0]
    y_pred = [11.0, 19.0, 32.0]

    report = evaluate_model_performance(y_true, y_pred, model_name="test_model_v1")

    assert report["model_name"] == "test_model_v1"
    assert report["sample_count"] == 3
    assert "metrics" in report
    assert "rmse" in report["metrics"]
    assert "mae" in report["metrics"]
    assert "r2" in report["metrics"]
    assert "telemetry" in report
    assert report["telemetry"]["status"] == "PASSED"
    assert report["telemetry"]["evaluation_latency_ms"] >= 0.0
