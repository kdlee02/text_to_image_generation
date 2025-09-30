"""
Image evaluation modules for aesthetic and human preference scoring.
"""

import torch
from PIL import Image
from aesthetic_predictor_v2_5 import convert_v2_5_from_siglip
import hpsv2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.optimization_config import AESTHETIC_WEIGHT, HPSV2_WEIGHT


class AestheticEvaluator:
    """Evaluates image aesthetic quality using aesthetic-predictor-v2-5."""

    def __init__(self):
        """Initialize the aesthetic evaluation model."""
        print("Loading aesthetic evaluation model...")
        self.model, self.preprocessor = convert_v2_5_from_siglip(
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        self.model = self.model.to(torch.bfloat16).cuda()
        print("✅ Aesthetic model loaded successfully!")

    def calculate_score(self, image: Image.Image) -> float:
        """Calculate aesthetic score for an image."""
        try:
            # Preprocess image
            pixel_values = (
                self.preprocessor(images=image, return_tensors="pt")
                .pixel_values.to(torch.bfloat16).cuda()
            )

            # Predict aesthetic score
            with torch.inference_mode():
                score = self.model(pixel_values).logits.squeeze().float().cpu().numpy()

            return float(score)

        except Exception as e:
            print(f"Error calculating aesthetic score: {str(e)}")
            return 0.0


class HPSv2Evaluator:
    """Evaluates human preference score using HPSv2."""

    def calculate_score(self, image: Image.Image, prompt: str) -> float:
        """Calculate HPSv2 score for an image and prompt pair."""
        try:
            hpscore = hpsv2.score(image, prompt, hps_version='v2.1')
            return float(hpscore[0])
        except Exception as e:
            print(f'Error calculating HPSv2: {e}')
            return 0.0


class CombinedEvaluator:
    """Combines aesthetic and HPSv2 evaluations."""

    def __init__(self):
        """Initialize both evaluators."""
        self.aesthetic_evaluator = AestheticEvaluator()
        self.hpsv2_evaluator = HPSv2Evaluator()

    def evaluate(self, image: Image.Image, prompt: str) -> dict:
        """Evaluate image with both metrics and return combined score."""
        aesthetic_score = self.aesthetic_evaluator.calculate_score(image)
        hpsv2_score = self.hpsv2_evaluator.calculate_score(image, prompt)
        
        # Combined score (weighted average)
        combined_score = (aesthetic_score * AESTHETIC_WEIGHT) + (hpsv2_score * HPSV2_WEIGHT)
        
        return {
            "aesthetic_score": aesthetic_score,
            "hpsv2_score": hpsv2_score,
            "combined_score": combined_score
        }