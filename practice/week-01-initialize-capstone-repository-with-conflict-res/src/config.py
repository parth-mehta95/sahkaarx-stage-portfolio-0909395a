"""
Configuration settings for AI Model Pipeline.
"""
from dataclasses import dataclass


@dataclass
class PipelineConfig:
    """Production pipeline configuration parameters."""
    model_name: str = "production-ai-regressor"
    version: str = "v1.0.0"
    random_seed: int = 42
    batch_size: int = 64
    normalization_strategy: str = "standard_scaler"
    enable_telemetry: bool = True
    log_level: str = "INFO"
