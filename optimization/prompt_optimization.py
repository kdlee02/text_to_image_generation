#!/usr/bin/env python3
"""
Main prompt optimization script using modular components.

This script provides a clean interface to the prompt optimization system,
using separate modules for image generation, evaluation, and optimization.
"""

from dotenv import load_dotenv
from src.core.optimization_engine import OptimizationEngine
from src.utils.utils import display_optimization_results, save_results_to_file

# Load environment variables
load_dotenv()


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