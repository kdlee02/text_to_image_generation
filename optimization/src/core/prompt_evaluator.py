"""
Prompt evaluation module that combines image generation and scoring.
"""

from typing import Dict
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.models.image_generator import ImageGenerator
from src.models.evaluators import CombinedEvaluator


class PromptEvaluator:
    """Evaluates prompts by generating images and calculating scores."""

    def __init__(self, api_key: str = None):
        """Initialize the prompt evaluator."""
        self.image_generator = ImageGenerator(api_key)
        self.evaluator = CombinedEvaluator()

    def evaluate_prompt(self, prompt: str) -> Dict:
        """Generate image and calculate both aesthetic and HPSv2 scores."""
        try:
            # Generate image
            image_url, metadata = self.image_generator.generate_image(prompt)
            
            # Download image for evaluation
            image = self.image_generator.download_image(image_url)
            
            # Calculate scores
            scores = self.evaluator.evaluate(image, prompt)
            
            return {
                "prompt": prompt,
                "image_url": image_url,
                "aesthetic_score": scores["aesthetic_score"],
                "hpscore": scores["hpsv2_score"],
                "combined_score": scores["combined_score"],
                "timestamp": metadata["timestamp"],
                "generation_time": metadata["generation_time"]
            }
            
        except Exception as e:
            print(f"❌ Error evaluating prompt: {str(e)}")
            return {
                "prompt": prompt,
                "error": str(e),
                "combined_score": 0.0
            }