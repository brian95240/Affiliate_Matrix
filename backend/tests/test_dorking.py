"""
Test script for validating the Google Dorking implementation.

This script tests the core functionality of the Google Dorking implementation
for the Affiliate Matrix project.
"""

import sys
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dorking.validation")

# Import dorking components directly with relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.dorking.core import DorkingEngine
from app.services.dorking.triggers import (
    EnvironmentalTriggerSystem,
    EnvironmentalContext
)
from app.services.dorking.strategies.affiliate_programs import (
    AffiliateFinderStrategy,
    CommissionAnalyzerStrategy
)
from app.services.dorking.strategies.competitor import (
    BacklinkAnalyzerStrategy,
    AffiliateStructureAnalyzerStrategy,
    ContentStrategyAnalyzerStrategy
)
from app.services.dorking.strategies.vulnerability import (
    ParameterScannerStrategy,
    CookieAnalyzerStrategy,
    AttributionModelAnalyzerStrategy,
    SecurityGapIdentifierStrategy
)
from app.services.dorking.strategies.content import (
    KeywordFinderStrategy,
    ContentStructureAnalyzerStrategy,
    UserIntentMapperStrategy,
    ConversionPathOptimizerStrategy
)

def test_dorking_engine():
    """Test the core dorking engine."""
    logger.info("Testing DorkingEngine...")
    
    engine = DorkingEngine()
    
    # Test query building
    query = engine.build_dork_query({
        "site": "example.com",
        "intext": "affiliate program"
    })
    logger.info(f"Built query: {query}")
    assert "site:example.com" in query
    assert "affiliate program" in query
    
    # Test query execution
    results = engine.execute_dork({
        "site": "example.com",
        "intext": "affiliate program"
    })
    logger.info(f"Query returned {len(results)} results")
    assert len(results) > 0
    
    logger.info("DorkingEngine tests passed")
    return True

def test_environmental_trigger_system():
    """Test the environmental trigger system."""
    logger.info("Testing EnvironmentalTriggerSystem...")
    
    trigger_system = EnvironmentalTriggerSystem()
    
    # Test context creation
    context = trigger_system.create_context(
        search_intent="new_programs",
        market_segment="health",
        competition_level="high",
        opportunity_type="discovery",
        time_sensitivity="urgent"
    )
    logger.info(f"Created context: {context}")
    assert context.search_intent == "new_programs"
    assert context.market_segment == "health"
    
    # Test strategy selection
    strategies = trigger_system.get_strategies_for_context(context)
    logger.info(f"Selected {len(strategies)} strategies")
    assert len(strategies) > 0
    
    logger.info("EnvironmentalTriggerSystem tests passed")
    return True

def test_affiliate_program_discovery():
    """Test the affiliate program discovery module."""
    logger.info("Testing Affiliate Program Discovery...")
    
    engine = DorkingEngine()
    
    # Test AffiliateFinderStrategy
    finder = AffiliateFinderStrategy(engine)
    results = finder.execute(niche="fitness")
    logger.info(f"AffiliateFinderStrategy returned {len(results)} results")
    assert len(results) > 0
    
    programs = finder.parse_program_details(results)
    logger.info(f"Parsed {len(programs)} affiliate programs")
    assert len(programs) > 0
    
    # Test CommissionAnalyzerStrategy
    analyzer = CommissionAnalyzerStrategy(engine)
    results = analyzer.execute()
    logger.info(f"CommissionAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    analysis = analyzer.analyze_commission_structure(results)
    logger.info(f"Commission structure analysis: {analysis}")
    assert "commission_types" in analysis
    
    logger.info("Affiliate Program Discovery tests passed")
    return True

def test_competitor_analysis():
    """Test the competitor analysis module."""
    logger.info("Testing Competitor Analysis...")
    
    engine = DorkingEngine()
    competitor_domain = "example.com"
    
    # Test BacklinkAnalyzerStrategy
    backlink_analyzer = BacklinkAnalyzerStrategy(engine)
    results = backlink_analyzer.execute(competitor_domain)
    logger.info(f"BacklinkAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    analysis = backlink_analyzer.analyze_backlink_profile(results)
    logger.info(f"Backlink profile analysis: {analysis}")
    assert "domain_types" in analysis
    
    # Test AffiliateStructureAnalyzerStrategy
    structure_analyzer = AffiliateStructureAnalyzerStrategy(engine)
    results = structure_analyzer.execute(competitor_domain)
    logger.info(f"AffiliateStructureAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    analysis = structure_analyzer.analyze_affiliate_structure(results)
    logger.info(f"Affiliate structure analysis: {analysis}")
    assert "network_distribution" in analysis
    
    # Test ContentStrategyAnalyzerStrategy
    content_analyzer = ContentStrategyAnalyzerStrategy(engine)
    results = content_analyzer.execute(competitor_domain)
    logger.info(f"ContentStrategyAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    analysis = content_analyzer.analyze_content_strategy(results)
    logger.info(f"Content strategy analysis: {analysis}")
    assert "content_distribution" in analysis
    
    logger.info("Competitor Analysis tests passed")
    return True

def test_vulnerability_assessment():
    """Test the vulnerability assessment module."""
    logger.info("Testing Vulnerability Assessment...")
    
    engine = DorkingEngine()
    target_domain = "example.com"
    
    # Test ParameterScannerStrategy
    parameter_scanner = ParameterScannerStrategy(engine)
    results = parameter_scanner.execute(target_domain)
    logger.info(f"ParameterScannerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    vulnerabilities = parameter_scanner.analyze_parameters(results)
    logger.info(f"Found {len(vulnerabilities)} parameter vulnerabilities")
    assert len(vulnerabilities) >= 0
    
    # Test CookieAnalyzerStrategy
    cookie_analyzer = CookieAnalyzerStrategy(engine)
    results = cookie_analyzer.execute(target_domain)
    logger.info(f"CookieAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    vulnerabilities = cookie_analyzer.analyze_cookies(results)
    logger.info(f"Found {len(vulnerabilities)} cookie vulnerabilities")
    assert len(vulnerabilities) >= 0
    
    # Test AttributionModelAnalyzerStrategy
    attribution_analyzer = AttributionModelAnalyzerStrategy(engine)
    results = attribution_analyzer.execute(target_domain)
    logger.info(f"AttributionModelAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    vulnerabilities = attribution_analyzer.analyze_attribution_model(results)
    logger.info(f"Found {len(vulnerabilities)} attribution vulnerabilities")
    assert len(vulnerabilities) >= 0
    
    # Test SecurityGapIdentifierStrategy
    security_gap_identifier = SecurityGapIdentifierStrategy(engine)
    results = security_gap_identifier.execute(target_domain)
    logger.info(f"SecurityGapIdentifierStrategy returned {len(results)} results")
    assert len(results) > 0
    
    security_gaps = security_gap_identifier.identify_security_gaps(results)
    logger.info(f"Found {len(security_gaps)} security gaps")
    assert len(security_gaps) >= 0
    
    logger.info("Vulnerability Assessment tests passed")
    return True

def test_content_gap_analysis():
    """Test the content gap analysis module."""
    logger.info("Testing Content Gap Analysis...")
    
    engine = DorkingEngine()
    niche = "travel"
    
    # Test KeywordFinderStrategy
    keyword_finder = KeywordFinderStrategy(engine)
    results = keyword_finder.execute(niche)
    logger.info(f"KeywordFinderStrategy returned {len(results)} results")
    assert len(results) > 0
    
    opportunities = keyword_finder.identify_opportunities(results, niche)
    logger.info(f"Found {len(opportunities)} keyword opportunities")
    assert len(opportunities) > 0
    
    # Test ContentStructureAnalyzerStrategy
    content_structure_analyzer = ContentStructureAnalyzerStrategy(engine)
    results = content_structure_analyzer.execute(niche)
    logger.info(f"ContentStructureAnalyzerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    analysis = content_structure_analyzer.analyze_content_structures(results)
    logger.info(f"Content structure analysis: {analysis}")
    assert "structure_distribution" in analysis
    
    # Test UserIntentMapperStrategy
    user_intent_mapper = UserIntentMapperStrategy(engine)
    results = user_intent_mapper.execute(niche)
    logger.info(f"UserIntentMapperStrategy returned {len(results)} results")
    assert len(results) > 0
    
    mapping = user_intent_mapper.map_user_intent(results, niche)
    logger.info(f"User intent mapping: {mapping}")
    assert "intent_distribution" in mapping
    
    # Test ConversionPathOptimizerStrategy
    conversion_path_optimizer = ConversionPathOptimizerStrategy(engine)
    results = conversion_path_optimizer.execute(niche)
    logger.info(f"ConversionPathOptimizerStrategy returned {len(results)} results")
    assert len(results) > 0
    
    optimization = conversion_path_optimizer.optimize_conversion_paths(results)
    logger.info(f"Conversion path optimization: {optimization}")
    assert "recommendations" in optimization
    
    logger.info("Content Gap Analysis tests passed")
    return True

def run_all_tests():
    """Run all validation tests."""
    logger.info("Starting validation tests for Google Dorking implementation...")
    
    tests = [
        test_dorking_engine,
        test_environmental_trigger_system,
        test_affiliate_program_discovery,
        test_competitor_analysis,
        test_vulnerability_assessment,
        test_content_gap_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            logger.error(f"Test {test.__name__} failed: {e}")
            results.append(False)
    
    success_count = sum(1 for r in results if r)
    logger.info(f"Validation complete: {success_count}/{len(tests)} tests passed")
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
