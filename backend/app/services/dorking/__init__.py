"""
Google Dorking services for the Affiliate Matrix project.

This package provides Google Dorking functionality with environmental triggers
that lazy load the correct dorking techniques and strategies based on context.
"""

from .core import DorkingEngine, DorkResult, RateLimiter, ResultParser
from .triggers import (
    EnvironmentalTriggerSystem,
    EnvironmentalContext,
    TriggerEvaluator,
    StrategyRepository,
    StrategySelector,
    TriggerType,
    DorkingStrategy
)

__all__ = [
    'DorkingEngine',
    'DorkResult',
    'RateLimiter',
    'ResultParser',
    'EnvironmentalTriggerSystem',
    'EnvironmentalContext',
    'TriggerEvaluator',
    'StrategyRepository',
    'StrategySelector',
    'TriggerType',
    'DorkingStrategy'
]
