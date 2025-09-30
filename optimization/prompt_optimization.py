#!/usr/bin/env python3
"""
Main prompt optimization script using modular components.

This script provides a clean interface to the prompt optimization system,
using separate modules for image generation, evaluation, and optimization.
"""

import sys
import os
from pathlib import Path

# Add the optimization directory to Python path
optimization_dir = Path(__file__).parent
sys.path.insert(0, str(optimization_dir))

from dotenv import load_dotenv
from src.core.optimization_engine import OptimizationEngine
from src.utils.utils import display_optimization_results, save_results_to_file

# Load environment variables from root directory
root_dir = optimization_dir.parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)


def optimize_prompt_iteratively(user_prompt: str, iterations: int = 5, api_key: str = None):
    """
    Main function to optimize prompts iteratively using DSPy.
    
    Args:
        user_prompt: Initial user prompt
        iterations: Number of optimization iterations (default: 5)
        api_key: Optional FAL AI API key
    
    Returns:
        Dictionary containing optimization results and final best prompt
    """
    engine = OptimizationEngine(api_key)
    return engine.optimize_iteratively(user_prompt, iterations)


def main():
    """Main interactive function."""
    print("🎨 AI-Powered Prompt Optimization System")
    print("=" * 50)
    
    # Get user input
    user_input = input("Enter your initial prompt: ")
    iterations = input("Number of iterations (default 5): ").strip()
    
    try:
        iterations = int(iterations) if iterations else 5
    except ValueError:
        iterations = 5
        print("Invalid input, using default 5 iterations.")
    
    # Run optimization
    print(f"\n🚀 Starting optimization with {iterations} iterations...")
    results = optimize_prompt_iteratively(user_input, iterations)
    
    # Display results
    display_optimization_results(results)
    
    # Save results to file
    filename = save_results_to_file(results)
    print(f"\n💾 Results saved to: {filename}")


if __name__ == "__main__":
    main()