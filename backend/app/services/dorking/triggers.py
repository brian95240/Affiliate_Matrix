"""
Environmental Trigger System for Google Dorking

This module implements the environmental trigger system that lazy loads
the appropriate dorking techniques based on context. It evaluates the
current environment and selects the most appropriate dorking strategy.
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
import importlib
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dorking.triggers")

class TriggerType(Enum):
    """Types of environmental triggers."""
    SEARCH_INTENT = "search_intent"
    MARKET_SEGMENT = "market_segment"
    COMPETITION_LEVEL = "competition_level"
    OPPORTUNITY_TYPE = "opportunity_type"
    RESOURCE_CONSTRAINT = "resource_constraint"
    TIME_SENSITIVITY = "time_sensitivity"

@dataclass
class EnvironmentalContext:
    """Data class representing the current environmental context."""
    search_intent: str
    market_segment: str
    competition_level: str
    opportunity_type: str
    resource_constraints: Dict[str, Any]
    time_sensitivity: str
    additional_factors: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the context to a dictionary."""
        return {
            "search_intent": self.search_intent,
            "market_segment": self.market_segment,
            "competition_level": self.competition_level,
            "opportunity_type": self.opportunity_type,
            "resource_constraints": self.resource_constraints,
            "time_sensitivity": self.time_sensitivity,
            "additional_factors": self.additional_factors or {}
        }

@dataclass
class DorkingStrategy:
    """Data class representing a dorking strategy."""
    name: str
    description: str
    module_path: str
    class_name: str
    priority: int
    applicable_contexts: List[Dict[str, Any]]
    
    def load_strategy_class(self):
        """Dynamically load the strategy class."""
        try:
            module = importlib.import_module(self.module_path)
            strategy_class = getattr(module, self.class_name)
            return strategy_class
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load strategy {self.name}: {e}")
            return None

class TriggerEvaluator:
    """Evaluates environmental triggers to determine which strategies to use."""
    
    def __init__(self):
        """Initialize the trigger evaluator."""
        self.triggers = {}
        self._register_default_triggers()
        
    def _register_default_triggers(self):
        """Register default triggers for each trigger type."""
        # Search Intent triggers
        self.register_trigger(
            TriggerType.SEARCH_INTENT,
            "new_programs",
            lambda ctx: ctx.search_intent == "new_programs"
        )
        self.register_trigger(
            TriggerType.SEARCH_INTENT,
            "competitor_analysis",
            lambda ctx: ctx.search_intent == "competitor_analysis"
        )
        self.register_trigger(
            TriggerType.SEARCH_INTENT,
            "vulnerability_assessment",
            lambda ctx: ctx.search_intent == "vulnerability_assessment"
        )
        self.register_trigger(
            TriggerType.SEARCH_INTENT,
            "content_gap",
            lambda ctx: ctx.search_intent == "content_gap"
        )
        
        # Market Segment triggers
        self.register_trigger(
            TriggerType.MARKET_SEGMENT,
            "high_competition",
            lambda ctx: ctx.competition_level == "high"
        )
        self.register_trigger(
            TriggerType.MARKET_SEGMENT,
            "medium_competition",
            lambda ctx: ctx.competition_level == "medium"
        )
        self.register_trigger(
            TriggerType.MARKET_SEGMENT,
            "low_competition",
            lambda ctx: ctx.competition_level == "low"
        )
        
        # Time Sensitivity triggers
        self.register_trigger(
            TriggerType.TIME_SENSITIVITY,
            "urgent",
            lambda ctx: ctx.time_sensitivity == "urgent"
        )
        self.register_trigger(
            TriggerType.TIME_SENSITIVITY,
            "normal",
            lambda ctx: ctx.time_sensitivity == "normal"
        )
        self.register_trigger(
            TriggerType.TIME_SENSITIVITY,
            "relaxed",
            lambda ctx: ctx.time_sensitivity == "relaxed"
        )
    
    def register_trigger(self, 
                        trigger_type: TriggerType, 
                        name: str, 
                        evaluation_func: Callable[[EnvironmentalContext], bool]):
        """
        Register a new trigger.
        
        Args:
            trigger_type: Type of the trigger
            name: Name of the trigger
            evaluation_func: Function that evaluates if the trigger is active
        """
        if trigger_type not in self.triggers:
            self.triggers[trigger_type] = {}
            
        self.triggers[trigger_type][name] = evaluation_func
        logger.debug(f"Registered trigger: {trigger_type.value}.{name}")
    
    def evaluate_context(self, context: EnvironmentalContext) -> Dict[TriggerType, List[str]]:
        """
        Evaluate which triggers are active for the given context.
        
        Args:
            context: The environmental context to evaluate
            
        Returns:
            Dictionary of active triggers by type
        """
        active_triggers = {}
        
        for trigger_type, triggers in self.triggers.items():
            active_for_type = []
            
            for name, eval_func in triggers.items():
                try:
                    if eval_func(context):
                        active_for_type.append(name)
                except Exception as e:
                    logger.error(f"Error evaluating trigger {trigger_type.value}.{name}: {e}")
            
            if active_for_type:
                active_triggers[trigger_type] = active_for_type
                
        logger.info(f"Active triggers: {active_triggers}")
        return active_triggers

class StrategyRepository:
    """Repository of available dorking strategies."""
    
    def __init__(self):
        """Initialize the strategy repository."""
        self.strategies = {}
        self._load_strategies()
        
    def _load_strategies(self):
        """Load available strategies from configuration."""
        # In a real implementation, this would load from a database or config file
        # For now, we'll hardcode some example strategies
        
        # Affiliate Program Discovery strategies
        self._register_strategy(DorkingStrategy(
            name="affiliate_program_finder",
            description="Finds new affiliate programs using URL patterns",
            module_path="affiliate_matrix.backend.app.services.dorking.strategies.affiliate_programs",
            class_name="AffiliateFinderStrategy",
            priority=10,
            applicable_contexts=[
                {"search_intent": "new_programs", "opportunity_type": "discovery"}
            ]
        ))
        
        self._register_strategy(DorkingStrategy(
            name="commission_structure_analyzer",
            description="Analyzes commission structures in affiliate programs",
            module_path="affiliate_matrix.backend.app.services.dorking.strategies.affiliate_programs",
            class_name="CommissionAnalyzerStrategy",
            priority=8,
            applicable_contexts=[
                {"search_intent": "new_programs", "opportunity_type": "optimization"}
            ]
        ))
        
        # Competitor Analysis strategies
        self._register_strategy(DorkingStrategy(
            name="competitor_backlink_analyzer",
            description="Analyzes competitor backlink patterns",
            module_path="affiliate_matrix.backend.app.services.dorking.strategies.competitor",
            class_name="BacklinkAnalyzerStrategy",
            priority=9,
            applicable_contexts=[
                {"search_intent": "competitor_analysis", "competition_level": "high"}
            ]
        ))
        
        # Vulnerability Assessment strategies
        self._register_strategy(DorkingStrategy(
            name="parameter_vulnerability_scanner",
            description="Scans for parameter manipulation vulnerabilities",
            module_path="affiliate_matrix.backend.app.services.dorking.strategies.vulnerability",
            class_name="ParameterScannerStrategy",
            priority=7,
            applicable_contexts=[
                {"search_intent": "vulnerability_assessment", "time_sensitivity": "urgent"}
            ]
        ))
        
        # Content Gap Analysis strategies
        self._register_strategy(DorkingStrategy(
            name="keyword_opportunity_finder",
            description="Finds keyword opportunities in the affiliate space",
            module_path="affiliate_matrix.backend.app.services.dorking.strategies.content",
            class_name="KeywordFinderStrategy",
            priority=6,
            applicable_contexts=[
                {"search_intent": "content_gap", "opportunity_type": "discovery"}
            ]
        ))
    
    def _register_strategy(self, strategy: DorkingStrategy):
        """
        Register a strategy in the repository.
        
        Args:
            strategy: The strategy to register
        """
        self.strategies[strategy.name] = strategy
        logger.debug(f"Registered strategy: {strategy.name}")
    
    def get_strategy(self, name: str) -> Optional[DorkingStrategy]:
        """
        Get a strategy by name.
        
        Args:
            name: Name of the strategy
            
        Returns:
            The strategy if found, None otherwise
        """
        return self.strategies.get(name)
    
    def get_all_strategies(self) -> List[DorkingStrategy]:
        """
        Get all registered strategies.
        
        Returns:
            List of all strategies
        """
        return list(self.strategies.values())

class StrategySelector:
    """Selects the appropriate dorking strategies based on active triggers."""
    
    def __init__(self, 
                repository: StrategyRepository,
                evaluator: TriggerEvaluator):
        """
        Initialize the strategy selector.
        
        Args:
            repository: Repository of available strategies
            evaluator: Trigger evaluator
        """
        self.repository = repository
        self.evaluator = evaluator
        
    def select_strategies(self, context: EnvironmentalContext) -> List[DorkingStrategy]:
        """
        Select appropriate strategies for the given context.
        
        Args:
            context: The environmental context
            
        Returns:
            List of selected strategies
        """
        # Evaluate which triggers are active
        active_triggers = self.evaluator.evaluate_context(context)
        
        # Get all available strategies
        all_strategies = self.repository.get_all_strategies()
        
        # Filter strategies based on active triggers
        selected_strategies = []
        context_dict = context.to_dict()
        
        for strategy in all_strategies:
            # Check if strategy is applicable to current context
            for applicable_context in strategy.applicable_contexts:
                matches = True
                
                for key, value in applicable_context.items():
                    if key in context_dict and context_dict[key] != value:
                        matches = False
                        break
                
                if matches:
                    selected_strategies.append(strategy)
                    break
        
        # Sort by priority (higher priority first)
        selected_strategies.sort(key=lambda s: s.priority, reverse=True)
        
        strategy_names = [s.name for s in selected_strategies]
        logger.info(f"Selected strategies: {strategy_names}")
        return selected_strategies

class EnvironmentalTriggerSystem:
    """Main class for the environmental trigger system."""
    
    def __init__(self):
        """Initialize the environmental trigger system."""
        self.repository = StrategyRepository()
        self.evaluator = TriggerEvaluator()
        self.selector = StrategySelector(self.repository, self.evaluator)
        logger.info("Environmental trigger system initialized")
        
    def get_strategies_for_context(self, context: EnvironmentalContext) -> List[DorkingStrategy]:
        """
        Get appropriate strategies for the given context.
        
        Args:
            context: The environmental context
            
        Returns:
            List of selected strategies
        """
        return self.selector.select_strategies(context)
    
    def create_context(self, **kwargs) -> EnvironmentalContext:
        """
        Create an environmental context from keyword arguments.
        
        Args:
            **kwargs: Context parameters
            
        Returns:
            EnvironmentalContext object
        """
        # Set defaults for required parameters
        defaults = {
            "search_intent": "new_programs",
            "market_segment": "general",
            "competition_level": "medium",
            "opportunity_type": "discovery",
            "resource_constraints": {"max_requests_per_minute": 10},
            "time_sensitivity": "normal",
            "additional_factors": {}
        }
        
        # Update defaults with provided values
        for key, value in kwargs.items():
            if key in defaults:
                if isinstance(defaults[key], dict) and isinstance(value, dict):
                    defaults[key].update(value)
                else:
                    defaults[key] = value
            else:
                if "additional_factors" not in defaults:
                    defaults["additional_factors"] = {}
                defaults["additional_factors"][key] = value
        
        return EnvironmentalContext(**defaults)
