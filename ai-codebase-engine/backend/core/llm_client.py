import os
from typing import List, Dict, Optional
import google.generativeai as genai

from config import settings

class LLMClient:
    """Wrapper for Google Gemini API interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            # Fallback or warning
            print("WARNING: Gemini API Key not found.")
            self.model = None
            return
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    def analyze_code(self, prompt: str, context: str, 
                    max_tokens: int = 4000) -> str:
        """Send code analysis request to Gemini."""
        if not self.model:
            return "LLM analysis is unavailable because GEMINI_API_KEY is not configured."
        
        full_prompt = f"{context}\n\n{prompt}\n\nProvide a detailed, technical analysis."
        
        response = self.model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
            )
        )
        
        try:
            return response.text
        except ValueError:
            return "Analysis was blocked by safety filters or returned empty."
    
    def answer_question(self, question: str, code_context: List[Dict]) -> str:
        """Answer question about codebase with RAG context."""
        if not self.model:
            return "LLM answers are unavailable because GEMINI_API_KEY is not configured."
        
        context_str = self._format_context(code_context)
        
        prompt = f"""You are analyzing a software repository. Here is relevant code context:

{context_str}

User Question: {question}

Provide a clear, accurate answer referencing specific files and functions."""
        
        response = self.model.generate_content(prompt)
        
        try:
            return response.text
        except ValueError:
            return "Answer was blocked by safety filters or returned empty."
    
    def generate_documentation(self, entity: Dict) -> str:
        """Generate documentation for code entity."""
        if not self.model:
            return "Documentation generation is unavailable because GEMINI_API_KEY is not configured."
        
        prompt = f"""Generate comprehensive documentation for this code entity:

Name: {entity.get('name', 'unknown')}
Type: {entity.get('type', 'unknown')}
File: {entity.get('file_path', 'unknown')}

Current docstring: {entity.get('docstring', 'None')}
Parameters: {entity.get('parameters', [])}
Dependencies: {entity.get('dependencies', [])}

Generate:
1. Clear description of purpose
2. Parameter explanations
3. Return value description
4. Usage example
5. Potential side effects or notes"""
        
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except ValueError:
            return "Documentation generation was blocked by safety filters or returned empty."
    
    def detect_security_issues(self, code_snippet: str, 
                               file_path: str) -> str:
        """Analyze code for security vulnerabilities."""
        if not self.model:
            return "[]"
        
        prompt = f"""Analyze this code for security vulnerabilities:

File: {file_path}

Code:
{code_snippet}

Identify:
1. SQL injection risks
2. Hardcoded credentials
3. Unsafe input handling
4. Authentication/authorization issues
5. Cryptography problems

Format as JSON with: issue_type, severity, line, description, fix"""
        
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except ValueError:
            return "[]"  # Return empty list JSON if blocked
    
    def explain_architecture(self, graph_data: Dict) -> str:
        """Explain overall system architecture."""
        if not self.model:
            return "Architecture explanation is unavailable because GEMINI_API_KEY is not configured."
        
        prompt = f"""Analyze this code dependency graph and explain the system architecture:

Graph data: {graph_data}

Provide:
1. High-level architecture pattern (MVC, microservices, etc.)
2. Key components and their roles
3. Data flow and communication patterns
4. Strengths and potential improvements"""
        
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except ValueError:
            return "Architecture explanation was blocked by safety filters or returned empty."
    
    def _format_context(self, context: List[Dict]) -> str:
        """Format RAG context for prompt."""
        formatted = []
        for item in context:
            document = item.get('document') or item.get('input') or item.get('text') or ''
            metadata = item.get('metadata') or {}
            source = metadata.get('file_path') or metadata.get('source') or ''
            header = f"---\nSource: {source}\n" if source else "---\n"
            formatted.append(f"{header}{document}\n")
        return "\n".join(formatted)
