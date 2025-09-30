"""
Main optimization engine that orchestrates the iterative prompt optimization process.
"""

from typing import Dict
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.core.prompt_evaluator import PromptEvaluator
from src.models.dspy_optimizer import DSPyManager
from config.optimization_config import DEFAULT_ITERATIONS


class OptimizationEngine:
    """Main engine for iterative prompt optimization."""

    def __init__(self, api_key: str = None):
        """Initialize the optimization engine."""
        self.prompt_evaluator = PromptEvaluator(api_key)
        self.dspy_manager = DSPyManager()

    def optimize_iteratively(self, user_prompt: str, iterations: int = DEFAULT_ITERATIONS) -> Dict:
        """
        Main function to optimize prompts iteratively using DSPy.
        
        Args:
            user_prompt: Initial user prompt
            iterations: Number of optimization iterations
        
        Returns:
            Dictionary containing optimization results and final best prompt
        """
        print(f"\n🚀 Starting iterative prompt optimization for: '{user_prompt}'")
        print("=" * 80)
        
        if not self.dspy_manager.enabled:
            print("❌ DSPy not available. Running single evaluation only.")
            result = self.prompt_evaluator.evaluate_prompt(user_prompt)
            return {
                "original_prompt": user_prompt,
                "final_prompt": user_prompt,
                "final_result": result,
                "optimization_history": [result],
                "best_score": result.get("combined_score", 0.0)
            }
        
        # Track optimization history
        optimization_history = []
        current_prompt = user_prompt
        best_result = None
        best_score = 0.0
        
        print(f"\n📊 Starting {iterations} optimization iterations...")
        
        for iteration in range(iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{iterations}")
            print("-" * 40)
            
            # Evaluate current prompt
            print(f"📝 Current prompt: '{current_prompt}'")
            result = self.prompt_evaluator.evaluate_prompt(current_prompt)
            
            if "error" not in result:
                current_score = result["combined_score"]
                print(f"📊 Scores - Aesthetic: {result['aesthetic_score']:.2f}, HPSv2: {result['hpscore']:.2f}, Combined: {current_score:.2f}")
                
                # Track best result
                if current_score > best_score:
                    best_score = current_score
                    best_result = result
                    print(f"🎉 New best score: {best_score:.2f}")
                
                optimization_history.append(result)
                
                # Generate optimized prompt for next iteration (except on last iteration)
                if iteration < iterations - 1:
                    print("🔧 Generating optimized prompt...")
                    
                    # Create feedback based on current performance
                    feedback = f"Current aesthetic score: {result['aesthetic_score']:.2f}, HPSv2 score: {result['hpscore']:.2f}"
                    if iteration > 0:
                        feedback += f" (Previous best: {best_score:.2f})"
                    
                    try:
                        optimized_prompt = self.dspy_manager.optimize_prompt(
                            original_prompt=user_prompt,
                            current_score=current_score,
                            feedback=feedback
                        )
                        current_prompt = optimized_prompt
                        print(f"✨ Next prompt: '{current_prompt}'")
                    except Exception as e:
                        print(f"⚠️ Error optimizing prompt: {str(e)}. Using current prompt.")
            else:
                print(f"❌ Error in iteration {iteration + 1}: {result['error']}")
                optimization_history.append(result)
        
        # Final results
        print(f"\n🏆 OPTIMIZATION COMPLETE!")
        print("=" * 80)
        print(f"Original prompt: {user_prompt}")
        print(f"Final best prompt: {best_result['prompt'] if best_result else user_prompt}")
        print(f"Best combined score: {best_score:.2f}")
        
        if best_result:
            print(f"Best aesthetic score: {best_result['aesthetic_score']:.2f}")
            print(f"Best HPSv2 score: {best_result['hpscore']:.2f}")
            print(f"Best image URL: {best_result['image_url']}")
        
        return {
            "original_prompt": user_prompt,
            "final_prompt": best_result["prompt"] if best_result else user_prompt,
            "final_result": best_result,
            "optimization_history": optimization_history,
            "best_score": best_score,
            "iterations_completed": len(optimization_history)
        }