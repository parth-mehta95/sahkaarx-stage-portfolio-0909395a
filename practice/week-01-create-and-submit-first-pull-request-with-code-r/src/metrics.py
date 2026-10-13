"""
AI Model Evaluation Metrics Module
Feature Branch: feature/model-evaluation-metrics
PR #12: feat(metrics): Add evaluation metrics and validation suite for AI model pipeline

This module provides standard regression and model evaluation metrics with input
validation, robust zero-division handling, and structured summary reporting.
"""

import time
from typing import Dict, Any, Union, List, Optional
import numpy as np


class EvaluationError(ValueError):
    """Raised when evaluation inputs fail validation checks."""
    pass


def _validate_inputs(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]]
) -> tuple[np.ndarray, np.ndarray]:
    """
    Validates and casts true and predicted target arrays.
    
    Args:
        y_true: Ground truth target values.
        y_pred: Estimated target values.
        
    Returns:
        Tuple of (y_true, y_pred) as 1D float64 NumPy arrays.
        
    Raises:
        EvaluationError: If arrays are empty, differ in length, or contain NaNs.
    """
    arr_true = np.asarray(y_true, dtype=np.float64)
    arr_pred = np.asarray(y_pred, dtype=np.float64)

    if arr_true.size == 0 or arr_pred.size == 0:
        raise EvaluationError("Evaluation arrays must not be empty.")

    if arr_true.shape != arr_pred.shape:
        raise EvaluationError(
            f"Shape mismatch: y_true shape {arr_true.shape} != y_pred shape {arr_pred.shape}"
        )

    if np.isnan(arr_true).any() or np.isnan(arr_pred).any():
        raise EvaluationError("Inputs contain NaN values; please clean data prior to evaluation.")

    return arr_true, arr_pred


def mean_squared_error(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]]
) -> float:
    """Calculates Mean Squared Error (MSE)."""
    t, p = _validate_inputs(y_true, y_pred)
    return float(np.mean((t - p) ** 2))


def root_mean_squared_error(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]]
) -> float:
    """Calculates Root Mean Squared Error (RMSE)."""
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mean_absolute_error(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]]
) -> float:
    """Calculates Mean Absolute Error (MAE)."""
    t, p = _validate_inputs(y_true, y_pred)
    return float(np.mean(np.abs(t - p)))


def r2_score(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]],
    epsilon: float = 1e-8
) -> float:
    """
    Calculates Coefficient of Determination (R^2 Score).
    
    Integrated from Code Review Feedback:
    Added epsilon guard to prevent ZeroDivisionError when y_true has zero variance.
    """
    t, p = _validate_inputs(y_true, y_pred)
    ss_res = np.sum((t - p) ** 2)
    ss_tot = np.sum((t - np.mean(t)) ** 2)

    if ss_tot < epsilon:
        # If true variance is zero, perfect predictions yield 1.0, otherwise 0.0
        return 1.0 if ss_res < epsilon else 0.0

    return float(1.0 - (ss_res / ss_tot))


def mean_absolute_percentage_error(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]],
    epsilon: float = 1e-8
) -> float:
    """Calculates Mean Absolute Percentage Error (MAPE) with division-by-zero protection."""
    t, p = _validate_inputs(y_true, y_pred)
    denom = np.where(np.abs(t) < epsilon, epsilon, np.abs(t))
    return float(np.mean(np.abs((t - p) / denom)) * 100.0)


def evaluate_model_performance(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]],
    model_name: Optional[str] = "ai_baseline_model"
) -> Dict[str, Any]:
    """
    Generates a structured evaluation report dictionary.
    
    Integrated from Code Review Feedback:
    Added execution latency profiling and structured output schema for MLflow / model card integration.
    """
    start_time = time.perf_counter()
    t, p = _validate_inputs(y_true, y_pred)

    metrics = {
        "rmse": root_mean_squared_error(t, p),
        "mae": mean_absolute_error(t, p),
        "mse": mean_squared_error(t, p),
        "r2": r2_score(t, p),
        "mape": mean_absolute_percentage_error(t, p),
    }

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "model_name": model_name,
        "sample_count": int(t.shape[0]),
        "metrics": metrics,
        "telemetry": {
            "evaluation_latency_ms": round(elapsed_ms, 3),
            "status": "PASSED"
        }
    }
