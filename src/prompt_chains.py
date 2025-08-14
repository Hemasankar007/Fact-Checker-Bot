from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Any

def create_prompt_chains(llm) -> Dict[str, Any]:
    # Initial Response Prompt
    initial_response_template = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(
            """You are a fact-checking assistant. Provide a preliminary answer to the following claim or question.
            Be concise but include key points that would need verification.
            
            Claim: {claim}
            
            Preliminary Answer:"""
        )
    ])
    
    # Assumption Verification Prompt
    assumption_verification_template = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(
            """Evaluate the truthfulness of this assumption based on the provided search results:
            
            Assumption: {assumption}
            
            Search Results:
            {search_results}
            
            Your evaluation should be one of:
            - TRUE: The assumption is supported by evidence
            - FALSE: The assumption is contradicted by evidence
            - UNCERTAIN: The evidence is inconclusive
            
            Provide a brief explanation for your evaluation.
            
            Evaluation:"""
        )
    ])
    
    # Final Synthesis Prompt
    final_synthesis_template = ChatPromptTemplate.from_messages([
        HumanMessagePromptTemplate.from_template(
            """Synthesize a final fact-checked response based on the original claim, initial response, and verified assumptions.
            
            Original Claim: {claim}
            Initial Response: {initial_response}
            
            Verified Assumptions:
            {verified_assumptions}
            
            Final Fact-Checked Response:"""
        )
    ])
    
    return {
        "initial_response": LLMChain(llm=llm, prompt=initial_response_template),
        "assumption_verification": LLMChain(llm=llm, prompt=assumption_verification_template),
        "final_synthesis": LLMChain(llm=llm, prompt=final_synthesis_template)
    }