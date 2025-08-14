from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from typing import List, Dict, Any
from .prompt_chains import create_prompt_chains
from .search_tools import WebSearchTool
from .utils import extract_assumptions, validate_assumptions
import logging
from config.settings import Settings

class FactCheckerBot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Settings.MODEL_NAME,
            temperature=Settings.TEMPERATURE,
            max_output_tokens=Settings.MAX_TOKENS,
            google_api_key=Settings.GOOGLE_API_KEY
        )
        self.prompt_chains = create_prompt_chains(self.llm)
        self.search_tool = WebSearchTool()
        
    def check_fact(self, claim: str) -> Dict[str, Any]:
        try:
            # Step 1: Initial Response
            initial_response = self._get_initial_response(claim)
            
            # Step 2: Assumption Extraction
            assumptions = extract_assumptions(initial_response)
            
            # Step 3: Verification Loop
            verified_assumptions = []
            for assumption in assumptions:
                verification = self._verify_assumption(assumption)
                verified_assumptions.append(verification)
            
            # Step 4: Final Synthesis
            final_response = self._synthesize_response(claim, initial_response, verified_assumptions)
            
            return {
                "claim": claim,
                "initial_response": initial_response,
                "assumptions": verified_assumptions,
                "final_response": final_response,
                "status": "completed"
            }
            
        except Exception as e:
            logging.error(f"Error in fact-checking: {str(e)}")
            print(f"Error in fact-checking: {str(e)}")
            return {
                "claim": claim,
                "error": str(e),
                "status": "failed"
            }
    
    def _get_initial_response(self, claim: str) -> str:
        chain = self.prompt_chains["initial_response"]
        return chain.run(claim=claim)
    
    def _verify_assumption(self, assumption: str) -> Dict[str, Any]:
        # Check if assumption is already a known fact
        validation = validate_assumptions(assumption)
        if validation["is_verified"]:
            return {
                "assumption": assumption,
                "verification": validation["verdict"],
                "evidence": "Known fact",
                "confidence": "high"
            }
        
        # If not, search for evidence
        search_results = self.search_tool.search(assumption)
        chain = self.prompt_chains["assumption_verification"]
        
        verification = chain.run(
            assumption=assumption,
            search_results=search_results
        )
        
        return {
            "assumption": assumption,
            "verification": verification,
            "evidence": search_results,
            "confidence": "medium" if search_results else "low"
        }
    
    def _synthesize_response(self, claim: str, initial_response: str, assumptions: List[Dict]) -> str:
        chain = self.prompt_chains["final_synthesis"]
        return chain.run(
            claim=claim,
            initial_response=initial_response,
            verified_assumptions=assumptions
        )