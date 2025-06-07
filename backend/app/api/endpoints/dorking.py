"""
Google Dorking API Integration for Affiliate Matrix

This module integrates the Google Dorking functionality with the Affiliate Matrix API.
It provides FastAPI endpoints for accessing the dorking capabilities.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ...services.dorking.core import DorkingEngine, DorkResult
from ...services.dorking.triggers import (
    EnvironmentalTriggerSystem, 
    EnvironmentalContext,
    DorkingStrategy
)

# Create router
router = APIRouter(
    prefix="/api/dorking",
    tags=["dorking"],
    responses={404: {"description": "Not found"}},
)

# Initialize dorking components
dorking_engine = DorkingEngine()
trigger_system = EnvironmentalTriggerSystem()

# Pydantic models for request/response
class DorkQueryRequest(BaseModel):
    query_components: Dict[str, str] = Field(
        ..., 
        description="Dictionary of operator:value pairs for the dork query"
    )
    context: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional context information for the query"
    )

class DorkResultResponse(BaseModel):
    url: str
    title: str
    snippet: str
    source: str
    query: str
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None

class EnvironmentalContextRequest(BaseModel):
    search_intent: str = Field(
        "new_programs", 
        description="What type of affiliate opportunity is being sought"
    )
    market_segment: str = Field(
        "general", 
        description="Industry or niche being targeted"
    )
    competition_level: str = Field(
        "medium", 
        description="Density of competitors in the space"
    )
    opportunity_type: str = Field(
        "discovery", 
        description="New program discovery vs optimization"
    )
    resource_constraints: Dict[str, Any] = Field(
        {"max_requests_per_minute": 10}, 
        description="Available computational resources"
    )
    time_sensitivity: str = Field(
        "normal", 
        description="Urgency of the search"
    )
    additional_factors: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional context factors"
    )

class DorkingStrategyResponse(BaseModel):
    name: str
    description: str
    module_path: str
    class_name: str
    priority: int

class AffiliateDiscoveryRequest(BaseModel):
    niche: Optional[str] = Field(
        None, 
        description="Optional niche to focus on"
    )
    context: EnvironmentalContextRequest = Field(
        ..., 
        description="Environmental context for the discovery"
    )

class CompetitorAnalysisRequest(BaseModel):
    competitor_domain: str = Field(
        ..., 
        description="Domain of the competitor to analyze"
    )
    context: EnvironmentalContextRequest = Field(
        ..., 
        description="Environmental context for the analysis"
    )

class VulnerabilityAssessmentRequest(BaseModel):
    target_domain: str = Field(
        ..., 
        description="Domain to assess for vulnerabilities"
    )
    context: EnvironmentalContextRequest = Field(
        ..., 
        description="Environmental context for the assessment"
    )

class ContentGapAnalysisRequest(BaseModel):
    niche: str = Field(
        ..., 
        description="The niche to analyze for content gaps"
    )
    competitor_domain: Optional[str] = Field(
        None, 
        description="Optional competitor domain to compare against"
    )
    context: EnvironmentalContextRequest = Field(
        ..., 
        description="Environmental context for the analysis"
    )

# API endpoints
@router.post("/execute", response_model=List[DorkResultResponse])
async def execute_dork_query(request: DorkQueryRequest):
    """
    Execute a Google dork query with the specified components.
    """
    try:
        results = dorking_engine.execute_dork(
            request.query_components,
            request.context
        )
        return [DorkResultResponse(**result.to_dict()) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/strategies", response_model=List[DorkingStrategyResponse])
async def get_strategies_for_context(request: EnvironmentalContextRequest):
    """
    Get appropriate dorking strategies for the given environmental context.
    """
    try:
        context = trigger_system.create_context(**request.dict())
        strategies = trigger_system.get_strategies_for_context(context)
        return [DorkingStrategyResponse(
            name=strategy.name,
            description=strategy.description,
            module_path=strategy.module_path,
            class_name=strategy.class_name,
            priority=strategy.priority
        ) for strategy in strategies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/affiliate-discovery", response_model=Dict[str, Any])
async def discover_affiliate_programs(request: AffiliateDiscoveryRequest):
    """
    Discover affiliate programs using Google dorking techniques.
    """
    try:
        # Import here to avoid circular imports
        from ...services.dorking.strategies.affiliate_programs import AffiliateFinderStrategy
        
        # Create context and get appropriate strategies
        context = trigger_system.create_context(**request.context.dict())
        
        # Initialize the strategy
        strategy = AffiliateFinderStrategy(dorking_engine)
        
        # Execute the strategy
        results = strategy.execute(request.niche)
        
        # Parse program details
        programs = strategy.parse_program_details(results)
        
        return {
            "results_count": len(results),
            "programs": [program.to_dict() for program in programs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/competitor-analysis", response_model=Dict[str, Any])
async def analyze_competitor(request: CompetitorAnalysisRequest):
    """
    Analyze competitor affiliate strategies using Google dorking techniques.
    """
    try:
        # Import here to avoid circular imports
        from ...services.dorking.strategies.competitor import (
            BacklinkAnalyzerStrategy,
            AffiliateStructureAnalyzerStrategy,
            ContentStrategyAnalyzerStrategy
        )
        
        # Create context
        context = trigger_system.create_context(**request.context.dict())
        
        # Initialize strategies
        backlink_strategy = BacklinkAnalyzerStrategy(dorking_engine)
        affiliate_structure_strategy = AffiliateStructureAnalyzerStrategy(dorking_engine)
        content_strategy = ContentStrategyAnalyzerStrategy(dorking_engine)
        
        # Execute strategies
        backlink_results = backlink_strategy.execute(request.competitor_domain)
        affiliate_structure_results = affiliate_structure_strategy.execute(request.competitor_domain)
        content_strategy_results = content_strategy.execute(request.competitor_domain)
        
        # Analyze results
        backlink_analysis = backlink_strategy.analyze_backlink_profile(backlink_results)
        affiliate_structure_analysis = affiliate_structure_strategy.analyze_affiliate_structure(affiliate_structure_results)
        content_strategy_analysis = content_strategy.analyze_content_strategy(content_strategy_results)
        
        return {
            "competitor_domain": request.competitor_domain,
            "backlink_analysis": backlink_analysis,
            "affiliate_structure_analysis": affiliate_structure_analysis,
            "content_strategy_analysis": content_strategy_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vulnerability-assessment", response_model=Dict[str, Any])
async def assess_vulnerabilities(request: VulnerabilityAssessmentRequest):
    """
    Assess vulnerabilities in affiliate systems using Google dorking techniques.
    """
    try:
        # Import here to avoid circular imports
        from ...services.dorking.strategies.vulnerability import (
            ParameterScannerStrategy,
            CookieAnalyzerStrategy,
            AttributionModelAnalyzerStrategy,
            SecurityGapIdentifierStrategy
        )
        
        # Create context
        context = trigger_system.create_context(**request.context.dict())
        
        # Initialize strategies
        parameter_scanner = ParameterScannerStrategy(dorking_engine)
        cookie_analyzer = CookieAnalyzerStrategy(dorking_engine)
        attribution_analyzer = AttributionModelAnalyzerStrategy(dorking_engine)
        security_gap_identifier = SecurityGapIdentifierStrategy(dorking_engine)
        
        # Execute strategies
        parameter_results = parameter_scanner.execute(request.target_domain)
        cookie_results = cookie_analyzer.execute(request.target_domain)
        attribution_results = attribution_analyzer.execute(request.target_domain)
        security_gap_results = security_gap_identifier.execute(request.target_domain)
        
        # Analyze results
        parameter_vulnerabilities = parameter_scanner.analyze_parameters(parameter_results)
        cookie_vulnerabilities = cookie_analyzer.analyze_cookies(cookie_results)
        attribution_vulnerabilities = attribution_analyzer.analyze_attribution_model(attribution_results)
        security_gaps = security_gap_identifier.identify_security_gaps(security_gap_results)
        
        # Determine overall risk level
        high_count = sum(1 for v in parameter_vulnerabilities if v.get("risk_level") == "high")
        high_count += sum(1 for v in cookie_vulnerabilities if v.get("risk_level") == "high")
        high_count += sum(1 for v in attribution_vulnerabilities if v.get("risk_level") == "high")
        high_count += sum(1 for v in security_gaps if v.get("risk_level") == "high")
        
        risk_level = "high" if high_count > 0 else "medium" if len(parameter_vulnerabilities) + len(cookie_vulnerabilities) + len(attribution_vulnerabilities) + len(security_gaps) > 3 else "low"
        
        return {
            "target_domain": request.target_domain,
            "parameter_vulnerabilities": parameter_vulnerabilities,
            "cookie_vulnerabilities": cookie_vulnerabilities,
            "attribution_vulnerabilities": attribution_vulnerabilities,
            "security_gaps": security_gaps,
            "risk_level": risk_level,
            "total_vulnerabilities": len(parameter_vulnerabilities) + len(cookie_vulnerabilities) + len(attribution_vulnerabilities) + len(security_gaps)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content-gap-analysis", response_model=Dict[str, Any])
async def analyze_content_gaps(request: ContentGapAnalysisRequest):
    """
    Analyze content gaps in the affiliate space using Google dorking techniques.
    """
    try:
        # Import here to avoid circular imports
        from ...services.dorking.strategies.content import (
            KeywordFinderStrategy,
            ContentStructureAnalyzerStrategy,
            UserIntentMapperStrategy,
            ConversionPathOptimizerStrategy
        )
        
        # Create context
        context = trigger_system.create_context(**request.context.dict())
        
        # Initialize strategies
        keyword_finder = KeywordFinderStrategy(dorking_engine)
        content_structure_analyzer = ContentStructureAnalyzerStrategy(dorking_engine)
        user_intent_mapper = UserIntentMapperStrategy(dorking_engine)
        conversion_path_optimizer = ConversionPathOptimizerStrategy(dorking_engine)
        
        # Execute strategies
        keyword_results = keyword_finder.execute(request.niche, request.competitor_domain)
        content_structure_results = content_structure_analyzer.execute(request.niche)
        user_intent_results = user_intent_mapper.execute(request.niche)
        conversion_path_results = conversion_path_optimizer.execute(request.niche)
        
        # Analyze results
        opportunities = keyword_finder.identify_opportunities(keyword_results, request.niche)
        content_structure_analysis = content_structure_analyzer.analyze_content_structures(content_structure_results)
        user_intent_mapping = user_intent_mapper.map_user_intent(user_intent_results, request.niche)
        conversion_path_optimization = conversion_path_optimizer.optimize_conversion_paths(conversion_path_results)
        
        return {
            "niche": request.niche,
            "competitor_domain": request.competitor_domain,
            "opportunities": [opp.to_dict() for opp in opportunities],
            "content_structure_analysis": content_structure_analysis,
            "user_intent_mapping": user_intent_mapping,
            "conversion_path_optimization": conversion_path_optimization
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
