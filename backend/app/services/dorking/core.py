"""
Core Google Dorking Engine for Affiliate Matrix

This module implements the core dorking algorithms that power the Affiliate Matrix
Google Dorking functionality. It provides a flexible and extensible framework for
executing Google dork queries while maintaining compliance with search engine terms.
"""

import time
import random
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dorking.core")

@dataclass
class DorkResult:
    """Data class representing a single dorking result."""
    url: str
    title: str
    snippet: str
    source: str
    query: str
    timestamp: float
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the result to a dictionary."""
        return {
            "url": self.url,
            "title": self.title,
            "snippet": self.snippet,
            "source": self.source,
            "query": self.query,
            "timestamp": self.timestamp,
            "metadata": self.metadata or {}
        }

class RateLimiter:
    """Rate limiter to prevent overloading search engines."""
    
    def __init__(self, 
                 requests_per_minute: int = 10, 
                 jitter: float = 0.2):
        """
        Initialize the rate limiter.
        
        Args:
            requests_per_minute: Maximum number of requests per minute
            jitter: Random jitter factor to add variability to request timing
        """
        self.min_interval = 60.0 / requests_per_minute
        self.jitter = jitter
        self.last_request_time = 0
        
    def wait(self) -> None:
        """Wait the appropriate amount of time before the next request."""
        if self.last_request_time == 0:
            self.last_request_time = time.time()
            return
            
        elapsed = time.time() - self.last_request_time
        wait_time = self.min_interval - elapsed
        
        # Add jitter to make the request pattern less predictable
        jitter_amount = random.uniform(-self.jitter * self.min_interval, 
                                      self.jitter * self.min_interval)
        wait_time += jitter_amount
        
        if wait_time > 0:
            logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
            
        self.last_request_time = time.time()

class ResultParser:
    """Parser for search engine results."""
    
    def parse_results(self, raw_results: Dict[str, Any], query: str) -> List[DorkResult]:
        """
        Parse raw search results into structured DorkResult objects.
        
        Args:
            raw_results: Raw results from search engine
            query: The original query string
            
        Returns:
            List of DorkResult objects
        """
        results = []
        timestamp = time.time()
        
        # Implementation will depend on the specific search API being used
        # This is a placeholder for the actual implementation
        if "items" in raw_results:
            for item in raw_results["items"]:
                result = DorkResult(
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    source="google",
                    query=query,
                    timestamp=timestamp,
                    metadata={
                        "position": item.get("position"),
                        "cached_page": item.get("cacheId"),
                        "mime_type": item.get("mime")
                    }
                )
                results.append(result)
                
        return results

class DorkingEngine:
    """Core engine for executing Google dork queries."""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 cx: Optional[str] = None,
                 requests_per_minute: int = 10):
        """
        Initialize the dorking engine.
        
        Args:
            api_key: Google Custom Search API key (optional)
            cx: Google Custom Search Engine ID (optional)
            requests_per_minute: Maximum requests per minute
        """
        self.api_key = api_key
        self.cx = cx
        self.rate_limiter = RateLimiter(requests_per_minute=requests_per_minute)
        self.result_parser = ResultParser()
        
        # Google dorking operators
        self.operators = {
            'site': 'Limit search to specific domain',
            'inurl': 'Search for URL containing specific text',
            'intitle': 'Search for pages with specific text in title',
            'intext': 'Search for pages containing specific text',
            'filetype': 'Search for specific file types',
            'link': 'Search for pages linking to specific URL',
            'related': 'Find related websites',
            'cache': 'View cached version of page',
            'info': 'Find information about a page',
            'daterange': 'Search within date range'
        }
        
        logger.info("DorkingEngine initialized")
        
    def build_dork_query(self, components: Dict[str, str]) -> str:
        """
        Build a dork query from components.
        
        Args:
            components: Dictionary of operator:value pairs
            
        Returns:
            Formatted dork query string
        """
        query_parts = []
        
        # Add each operator component to the query
        for operator, value in components.items():
            if operator in self.operators and value:
                if operator == "intext":
                    # For intext, we don't need the operator for basic text search
                    query_parts.append(f"{value}")
                else:
                    query_parts.append(f"{operator}:{value}")
        
        return " ".join(query_parts)
    
    def execute_dork(self, 
                    dork_query: Union[str, Dict[str, str]], 
                    context: Optional[Dict[str, Any]] = None) -> List[DorkResult]:
        """
        Execute a dork query and return results.
        
        Args:
            dork_query: Either a pre-formatted query string or components dict
            context: Optional context information for the query
            
        Returns:
            List of DorkResult objects
        """
        # Convert components dict to query string if needed
        if isinstance(dork_query, dict):
            query = self.build_dork_query(dork_query)
        else:
            query = dork_query
            
        logger.info(f"Executing dork query: {query}")
        
        # Apply rate limiting
        self.rate_limiter.wait()
        
        # In a real implementation, this would call the search API
        # For now, we'll simulate results
        raw_results = self._simulate_search_results(query)
        
        # Parse the results
        results = self.result_parser.parse_results(raw_results, query)
        
        logger.info(f"Dork query returned {len(results)} results")
        return results
    
    def _simulate_search_results(self, query: str) -> Dict[str, Any]:
        """
        Simulate search results for development and testing.
        
        Args:
            query: The search query
            
        Returns:
            Simulated raw search results
        """
        # This is a placeholder that simulates search results
        # In production, this would be replaced with actual API calls
        
        # Generate some fake results based on the query
        items = []
        domains = ["example.com", "affiliate-program.com", "marketing-partners.net", 
                  "affiliates.example.org", "partner-network.com"]
        
        for i in range(5):  # Simulate 5 results
            domain = random.choice(domains)
            path = f"/program/{i}" if "program" in query else "/affiliate"
            
            items.append({
                "link": f"https://{domain}{path}",
                "title": f"Affiliate Program {i+1} - {domain}",
                "snippet": f"Join our affiliate program and earn commissions. {query}",
                "position": i+1,
                "cacheId": f"cache_{domain}_{i}",
                "mime": "text/html"
            })
            
        return {
            "items": items,
            "searchInformation": {
                "totalResults": len(items),
                "searchTime": 0.5
            }
        }
