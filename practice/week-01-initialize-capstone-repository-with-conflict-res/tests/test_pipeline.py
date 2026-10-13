"""
Unit tests validating ModelPipeline functionality after merge conflict resolution.
"""
import numpy as np
import pytest
from src.model_pipeline import ModelPipeline


def test_pipeline_initialization():
    pipeline = ModelPipeline()
    assert pipeline.mean_ is None
    assert pipeline.std_ is None


def test_pipeline_preprocessing_values():
    pipeline = ModelPipeline()
    sample_data = [
        [10.0, 20.0, 30.0],
        [20.0, 30.0, 40.0],
        [30.0, 40.0, 50.0]
    ]
    processed = pipeline.preprocess_data(sample_data)
    assert processed.shape == (3, 3)
    # Check zero mean across columns
    assert np.allclose(processed.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-5)


def test_pipeline_prediction_shape():
    pipeline = ModelPipeline()
    sample_data = [
        [1.0, 2.0],
        [3.0, 4.0]
    ]
    processed = pipeline.preprocess_data(sample_data)
    predictions = pipeline.predict(processed)
    assert len(predictions) == 2


def test_pipeline_empty_handling():
    pipeline = ModelPipeline()
    processed = pipeline.preprocess_data([])
    assert processed.size == 0
    predictions = pipeline.predict(processed)
    assert len(predictions) == 0
