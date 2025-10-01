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
            "prompt_to_optimize -> optimized_prompt"
        )
    
    def forward(self, original_prompt: str, current_score: float, feedback: str = "") -> str:
        """Optimize a prompt based on current performance and feedback."""

        optimization_prompt = f"""Enhance this image generation prompt to achieve higher aesthetic and HPSv2 scores.

    Original prompt: {original_prompt}
    Current score: {current_score:.2f}/10

    Feedback from last attempt: {feedback}

    Enhancement instructions:
    - Keep the core concept but add visual details
    - Include artistic style terms: "highly detailed", "professional photography", "award-winning"
    - Add lighting terms: "dramatic lighting", "perfect lighting", "golden hour"
    - Add composition terms: "perfect composition", "rule of thirds"
    - Add quality terms: "8k resolution", "masterpiece", "trending on artstation"
    - Keep it concise but descriptive

    Enhanced prompt:"""

        result = self.optimize_prompt(prompt_to_optimize=optimization_prompt)
        optimized = result.optimized_prompt.strip()
        return optimized


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
            
            # Use the correct DSPy LM configuration for Upstage Solar Pro 2
            # DSPy uses LiteLLM under the hood, so we can specify the model directly
            lm = dspy.LM(model=DSPY_MODEL, api_key=openai_api_key)
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