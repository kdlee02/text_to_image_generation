"""
AI-Powered Prompt Optimization System

A modular system for optimizing image generation prompts using DSPy,
aesthetic evaluation, and human preference scoring.
"""

from .src.core.optimization_engine import OptimizationEngine
from .src.core.prompt_evaluator import PromptEvaluator
from .src.models.image_generator import ImageGenerator
from .src.models.evaluators import AestheticEvaluator, HPSv2Evaluator, CombinedEvaluator
from .src.models.dspy_optimizer import PromptOptimizer, DSPyManager
from .src.utils.utils import display_optimization_results, save_results_to_file, load_results_from_file

__version__ = "1.0.0"
__author__ = "AI Optimization Team"

# Main convenience function
def optimize_prompt(prompt: str, iterations: int = 5, api_key: str = None):
    """
    Convenience function to optimize a prompt.
    
    Args:
        prompt: Initial prompt to optimize
        iterations: Number of optimization iterations
        api_key: Optional FAL AI API key
    
    Returns:
        Optimization results dictionary
    """
    engine = OptimizationEngine(api_key)
    return engine.optimize_iteratively(prompt, iterations)