"""
Utility functions for the optimization system.
"""

import json
from datetime import datetime
from typing import Dict


def display_optimization_results(results: Dict):
    """Display optimization results in a formatted way."""
    print(f"\n📈 OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Original Prompt: {results['original_prompt']}")
    print(f"Final Prompt: {results['final_prompt']}")
    print(f"Best Score: {results['best_score']:.2f}")
    print(f"Iterations: {results['iterations_completed']}")
    
    if results['final_result']:
        print(f"\n🎨 FINAL IMAGE DETAILS:")
        print(f"Aesthetic Score: {results['final_result']['aesthetic_score']:.2f}")
        print(f"HPSv2 Score: {results['final_result']['hpscore']:.2f}")
        print(f"Image URL: {results['final_result']['image_url']}")
    
    print(f"\n📊 ITERATION HISTORY:")
    for i, result in enumerate(results['optimization_history']):
        if "error" not in result:
            print(f"  {i+1}. Score: {result['combined_score']:.2f} | Prompt: {result['prompt'][:60]}...")
        else:
            print(f"  {i+1}. ERROR: {result['error']}")


def save_results_to_file(results: Dict, filename: str = None) -> str:
    """Save optimization results to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"optimization_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    return filename


def load_results_from_file(filename: str) -> Dict:
    """Load optimization results from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def compare_results(results_list: list) -> Dict:
    """Compare multiple optimization results."""
    if not results_list:
        return {}
    
    best_overall = max(results_list, key=lambda x: x.get('best_score', 0))
    
    comparison = {
        "total_runs": len(results_list),
        "best_overall_score": best_overall.get('best_score', 0),
        "best_overall_prompt": best_overall.get('final_prompt', ''),
        "average_score": sum(r.get('best_score', 0) for r in results_list) / len(results_list),
        "score_range": {
            "min": min(r.get('best_score', 0) for r in results_list),
            "max": max(r.get('best_score', 0) for r in results_list)
        }
    }
    
    return comparison