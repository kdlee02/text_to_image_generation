#!/usr/bin/env python3
"""
Example usage of the modular prompt optimization system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.optimization_engine import OptimizationEngine
from src.core.prompt_evaluator import PromptEvaluator
from src.utils.utils import display_optimization_results, save_results_to_file


def example_basic_optimization():
    """Example of basic prompt optimization."""
    print("📝 Example 1: Basic Optimization")
    print("=" * 40)
    
    # Initialize the optimization engine
    engine = OptimizationEngine()
    
    # Optimize a simple prompt
    prompt = "a cat sitting in a garden"
    results = engine.optimize_iteratively(prompt, iterations=3)
    
    # Display results
    display_optimization_results(results)
    
    return results


def example_single_evaluation():
    """Example of evaluating a single prompt without optimization."""
    print("\n📊 Example 2: Single Prompt Evaluation")
    print("=" * 40)
    
    # Initialize the prompt evaluator
    evaluator = PromptEvaluator()
    
    # Evaluate a prompt
    prompt = "a futuristic cityscape at night, neon lights, cyberpunk style"
    result = evaluator.evaluate_prompt(prompt)
    
    if "error" not in result:
        print(f"Prompt: {result['prompt']}")
        print(f"Aesthetic Score: {result['aesthetic_score']:.2f}")
        print(f"HPSv2 Score: {result['hpscore']:.2f}")
        print(f"Combined Score: {result['combined_score']:.2f}")
        print(f"Image URL: {result['image_url']}")
    else:
        print(f"Error: {result['error']}")
    
    return result


def example_batch_optimization():
    """Example of optimizing multiple prompts."""
    print("\n🔄 Example 3: Batch Optimization")
    print("=" * 40)
    
    prompts = [
        "a mountain landscape",
        "abstract geometric art",
        "a portrait of an elderly person"
    ]
    
    engine = OptimizationEngine()
    all_results = []
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Optimizing prompt {i}/{len(prompts)}: {prompt} ---")
        
        try:
            results = engine.optimize_iteratively(prompt, iterations=2)
            all_results.append(results)
            
            print(f"✅ Original: {results['original_prompt']}")
            print(f"✅ Optimized: {results['final_prompt']}")
            print(f"✅ Score improvement: {results['best_score']:.2f}")
            
        except Exception as e:
            print(f"❌ Failed to optimize '{prompt}': {str(e)}")
    
    return all_results


def example_custom_configuration():
    """Example of using custom configuration."""
    print("\n⚙️ Example 4: Custom Configuration")
    print("=" * 40)
    
    # You can modify optimization_config.py or override settings
    from config.optimization_config import DEFAULT_ITERATIONS, AESTHETIC_WEIGHT, HPSV2_WEIGHT
    
    print(f"Current configuration:")
    print(f"  Default iterations: {DEFAULT_ITERATIONS}")
    print(f"  Aesthetic weight: {AESTHETIC_WEIGHT}")
    print(f"  HPSv2 weight: {HPSV2_WEIGHT}")
    
    # Example with custom iterations
    engine = OptimizationEngine()
    prompt = "a serene lake at dawn"
    
    print(f"\nOptimizing with custom settings...")
    results = engine.optimize_iteratively(prompt, iterations=2)
    
    print(f"Final score: {results['best_score']:.2f}")
    
    return results


def main():
    """Run all examples."""
    print("🎨 Modular Prompt Optimization Examples")
    print("=" * 60)
    
    examples = [
        example_basic_optimization,
        example_single_evaluation,
        example_batch_optimization,
        example_custom_configuration
    ]
    
    results = []
    
    for example_func in examples:
        try:
            result = example_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Example failed: {str(e)}")
            results.append(None)
    
    print(f"\n{'='*60}")
    print("🏆 EXAMPLES SUMMARY")
    print("=" * 60)
    print(f"Completed {len([r for r in results if r is not None])}/{len(examples)} examples successfully")
    
    # Save the first successful optimization result
    successful_results = [r for r in results if r is not None and isinstance(r, dict) and 'final_prompt' in r]
    if successful_results:
        filename = save_results_to_file(successful_results[0])
        print(f"💾 Sample results saved to: {filename}")


if __name__ == "__main__":
    main()