"""
DSPy-based prompt optimization module.
"""

import os
import dspy
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.optimization_config import DSPY_MODEL


class PromptOptimizer(dspy.Module):
    """DSPy module for optimizing image generation prompts."""
    
    def __init__(self):
        super().__init__()
        self.optimize_prompt = dspy.ChainOfThought(
            "original_prompt, current_score, feedback -> optimized_prompt"
        )
    
    def forward(self, original_prompt: str, current_score: float, feedback: str = "") -> str:
        """Optimize a prompt based on current performance."""
        optimization_context = f"""
        You are an expert at optimizing prompts for AI image generation to achieve higher aesthetic and HPSv2 scores.
        
        Original prompt: {original_prompt}
        Current combined score: {current_score:.2f}
        Feedback: {feedback}
        
        Guidelines for optimization:
        1. Keep the core concept but enhance visual details
        2. Maintain coherence and avoid contradictory terms
        3. Keep the prompt concise but descriptive
        
        Generate an improved version of the prompt that will likely achieve higher aesthetic and HPSv2 scores.
        """
        
        result = self.optimize_prompt(
            original_prompt=original_prompt,
            current_score=current_score,
            feedback=optimization_context
        )
        
        return result.optimized_prompt


class DSPyManager:
    """Manages DSPy configuration and optimization."""

    def __init__(self):
        """Initialize DSPy with OpenAI model."""
        self.enabled = self._setup_dspy()
        self.optimizer = PromptOptimizer() if self.enabled else None

    def _setup_dspy(self) -> bool:
        """Setup DSPy with OpenAI model for prompt optimization."""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                print("⚠️ Warning: OPENAI_API_KEY not found. DSPy optimization will be disabled.")
                return False
            
            lm = dspy.OpenAI(model=DSPY_MODEL, api_key=openai_api_key)
            dspy.configure(lm=lm)
            print("✅ DSPy configured successfully!")
            return True
            
        except Exception as e:
            print(f"⚠️ Warning: Failed to setup DSPy: {str(e)}. Optimization will be disabled.")
            return False

    def optimize_prompt(self, original_prompt: str, current_score: float, feedback: str = "") -> str:
        """Optimize a prompt using DSPy."""
        if not self.enabled:
            raise RuntimeError("DSPy is not enabled. Check OpenAI API key configuration.")
        
        return self.optimizer.forward(original_prompt, current_score, feedback)