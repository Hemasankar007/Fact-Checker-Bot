from typing import List, Dict, Any
import re

def extract_assumptions(response: str) -> List[str]:
    """Extract assumptions from the initial response"""
    prompt = f"""Extract all factual assumptions made in the following text. 
    List each assumption on a separate line.
    
    Text:
    {response}
    
    Assumptions:"""
    
    # In a real implementation, this would use an LLM chain
    # For demo purposes, we'll use a simple regex
    assumptions = re.findall(r'(?i)(?:assume|assuming|presume|presuming|probably|likely|perhaps)\s+(.*?)[.,;]', response)
    return [a.strip() for a in assumptions if a.strip()]

def validate_assumptions(assumption: str) -> Dict[str, Any]:
    """Check if an assumption is a known fact"""
    known_facts = {
        "the capital of France is Paris": True,
        "the Earth orbits the Sun": True,
        "water boils at 100 degrees Celsius at sea level": True
    }
    
    lower_assumption = assumption.lower()
    for fact, verdict in known_facts.items():
        if fact in lower_assumption:
            return {
                "is_verified": True,
                "verdict": "TRUE" if verdict else "FALSE"
            }
    
    return {"is_verified": False, "verdict": "UNCERTAIN"}