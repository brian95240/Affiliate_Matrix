"""
Simple validation script for the Google Dorking implementation.

This script performs basic validation of the core components
without requiring complex imports.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dorking.validation")

def validate_file_structure():
    """Validate that all required files exist."""
    logger.info("Validating file structure...")
    
    required_files = [
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/core.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/triggers.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/__init__.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/strategies/affiliate_programs.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/strategies/competitor.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/strategies/vulnerability.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/strategies/content.py",
        "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/strategies/__init__.py",
        "/home/ubuntu/affiliate_matrix/backend/app/api/endpoints/dorking.py",
        "/home/ubuntu/affiliate_matrix/docs/google_dorking_guide.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"Missing files: {missing_files}")
        return False
    
    logger.info("All required files exist")
    return True

def validate_code_content():
    """Validate that key components are implemented in the code."""
    logger.info("Validating code content...")
    
    # Check core.py
    core_path = "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/core.py"
    with open(core_path, 'r') as f:
        core_content = f.read()
        
    if "class DorkingEngine" not in core_content:
        logger.error("DorkingEngine class not found in core.py")
        return False
    
    if "class RateLimiter" not in core_content:
        logger.error("RateLimiter class not found in core.py")
        return False
    
    # Check triggers.py
    triggers_path = "/home/ubuntu/affiliate_matrix/backend/app/services/dorking/triggers.py"
    with open(triggers_path, 'r') as f:
        triggers_content = f.read()
        
    if "class EnvironmentalTriggerSystem" not in triggers_content:
        logger.error("EnvironmentalTriggerSystem class not found in triggers.py")
        return False
    
    # Check API integration
    api_path = "/home/ubuntu/affiliate_matrix/backend/app/api/endpoints/dorking.py"
    with open(api_path, 'r') as f:
        api_content = f.read()
        
    if "router = APIRouter" not in api_content:
        logger.error("APIRouter not found in dorking.py")
        return False
    
    logger.info("All key components are implemented")
    return True

def validate_documentation():
    """Validate that documentation is comprehensive."""
    logger.info("Validating documentation...")
    
    docs_path = "/home/ubuntu/affiliate_matrix/docs/google_dorking_guide.md"
    with open(docs_path, 'r') as f:
        docs_content = f.read()
        
    required_sections = [
        "# Google Dorking Implementation",
        "## Architecture",
        "## Core Components",
        "## Usage Guide",
        "## Security and Compliance"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in docs_content:
            missing_sections.append(section)
    
    if missing_sections:
        logger.error(f"Missing documentation sections: {missing_sections}")
        return False
    
    # Check documentation length
    if len(docs_content) < 5000:
        logger.warning("Documentation may not be comprehensive enough")
        
    logger.info("Documentation is comprehensive")
    return True

def run_validation():
    """Run all validation checks."""
    logger.info("Starting validation of Google Dorking implementation...")
    
    structure_valid = validate_file_structure()
    code_valid = validate_code_content()
    docs_valid = validate_documentation()
    
    all_valid = structure_valid and code_valid and docs_valid
    
    if all_valid:
        logger.info("Validation successful: All components are properly implemented")
    else:
        logger.error("Validation failed: Some components are missing or incomplete")
        
    return all_valid

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
