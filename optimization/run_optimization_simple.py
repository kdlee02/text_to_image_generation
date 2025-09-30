#!/usr/bin/env python3
"""
Simplified prompt optimization script that works around import issues.
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

# Add the optimization directory to Python path
optimization_dir = Path(__file__).parent
sys.path.insert(0, str(optimization_dir))

# Load environment
from dotenv import load_dotenv
root_dir = optimization_dir.parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)

# Import required libraries
import fal_client
import requests
import tempfile
from PIL import Image
import torch
from aesthetic_predictor_v2_5 import convert_v2_5_from_siglip
import hpsv2
import dspy

# Configuration
DEFAULT_MODEL = "fal-ai/imagen4/preview"
IMAGE_SIZE = "square_hd"
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 7.5
AESTHETIC_WEIGHT = 0.5
HPSV2_WEIGHT = 0.5
DEFAULT_ITERATIONS = 5


class SimpleImageGenerator:
    """Simple image generator using FAL AI."""
    
    def __init__(self):
        if not os.getenv('FAL_KEY'):
            raise ValueError("FAL_KEY environment variable required")
    
    def generate_image(self, prompt: str) -> Tuple[str, Dict]:
        """Generate image using FAL AI."""
        start_time = time.time()
        
        response = fal_client.run(
            DEFAULT_MODEL,
            arguments={
                "prompt": prompt,
                "image_size": IMAGE_SIZE,
                "num_inference_steps": NUM_INFERENCE_STEPS,
                "guidance_scale": GUIDANCE_SCALE
            }
        )
        
        end_time = time.time()
        
        if response and "images" in response and len(response["images"]) > 0:
            image_url = response["images"][0]["url"]
            metadata = {
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat(),
                "generation_time": end_time - start_time,
                "response": response
            }
            return image_url, metadata
        else:
            raise Exception("No image generated in response")
    
    def download_image(self, url: str) -> Image.Image:
        """Download image from URL."""
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        image = Image.open(tmp_path).convert("RGB")
        os.unlink(tmp_path)
        return image


class SimpleEvaluator:
    """Simple evaluator for aesthetic and HPSv2 scores."""
    
    def __init__(self):
        print("Loading aesthetic evaluation model...")
        self.aesthetic_model, self.preprocessor = convert_v2_5_from_siglip(
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        self.aesthetic_model = self.aesthetic_model.to(torch.bfloat16).cuda()
        print("✅ Aesthetic model loaded successfully!")
    
    def calculate_aesthetic_score(self, image: Image.Image) -> float:
        """Calculate aesthetic score."""
        try:
            pixel_values = (
                self.preprocessor(images=image, return_tensors="pt")
                .pixel_values.to(torch.bfloat16).cuda()
            )
            
            with torch.inference_mode():
                score = self.aesthetic_model(pixel_values).logits.squeeze().float().cpu().numpy()
            
            return float(score)
        except Exception as e:
            print(f"Error calculating aesthetic score: {str(e)}")
            return 0.0
    
    def calculate_hpsv2_score(self, image: Image.Image, prompt: str) -> float:
        """Calculate HPSv2 score."""
        try:
            hpscore = hpsv2.score(image, prompt, hps_version='v2.1')
            return float(hpscore[0])
        except Exception as e:
            print(f'Error calculating HPSv2: {e}')
            return 0.0
    
    def evaluate(self, image: Image.Image, prompt: str) -> Dict:
        """Evaluate image with both metrics."""
        aesthetic_score = self.calculate_aesthetic_score(image)
        hpsv2_score = self.calculate_hpsv2_score(image, prompt)
        combined_score = (aesthetic_score * AESTHETIC_WEIGHT) + (hpsv2_score * HPSV2_WEIGHT)
        
        return {
            "aesthetic_score": aesthetic_score,
            "hpsv2_score": hpsv2_score,
            "combined_score": combined_score
        }


class SimpleOptimizer:
    """Simple DSPy-based prompt optimizer."""
    
    def __init__(self):
        self.enabled = self._setup_dspy()
        if self.enabled:
            self.optimize_prompt = dspy.ChainOfThought(
                "original_prompt, current_score, feedback -> optimized_prompt"
            )
    
    def _setup_dspy(self) -> bool:
        """Setup DSPy with OpenAI."""
        try:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                print("⚠️ Warning: OPENAI_API_KEY not found. DSPy optimization will be disabled.")
                return False
            
            lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=openai_api_key)
            dspy.configure(lm=lm)
            print("✅ DSPy configured successfully!")
            return True
        except Exception as e:
            print(f"⚠️ Warning: Failed to setup DSPy: {str(e)}. Optimization will be disabled.")
            return False
    
    def optimize(self, original_prompt: str, current_score: float, feedback: str = "") -> str:
        """Optimize a prompt using DSPy."""
        if not self.enabled:
            return original_prompt
        
        optimization_context = f"""
        You are an expert at optimizing prompts for AI image generation to achieve higher aesthetic and HPSv2 scores.
        
        Original prompt: {original_prompt}
        Current combined score: {current_score:.2f}
        Feedback: {feedback}
        
        Guidelines for optimization:
        1. Keep the core concept but enhance visual details
        2. Add artistic style descriptors (e.g., "highly detailed", "professional photography", "award-winning")
        3. Include lighting and composition terms (e.g., "dramatic lighting", "perfect composition")
        4. Add quality enhancers (e.g., "8k resolution", "masterpiece", "trending on artstation")
        5. Maintain coherence and avoid contradictory terms
        6. Keep the prompt concise but descriptive
        
        Generate an improved version of the prompt that will likely achieve higher aesthetic and HPSv2 scores.
        """
        
        try:
            result = self.optimize_prompt(
                original_prompt=original_prompt,
                current_score=current_score,
                feedback=optimization_context
            )
            return result.optimized_prompt
        except Exception as e:
            print(f"Error optimizing prompt: {str(e)}")
            return original_prompt


def run_optimization(user_prompt: str, iterations: int = DEFAULT_ITERATIONS):
    """Run the complete optimization process."""
    print(f"\n🚀 Starting iterative prompt optimization for: '{user_prompt}'")
    print("=" * 80)
    
    # Initialize components
    generator = SimpleImageGenerator()
    evaluator = SimpleEvaluator()
    optimizer = SimpleOptimizer()
    
    if not optimizer.enabled:
        print("❌ DSPy not available. Running single evaluation only.")
        iterations = 1
    
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
        
        try:
            # Generate image
            image_url, metadata = generator.generate_image(current_prompt)
            
            # Download image for evaluation
            image = generator.download_image(image_url)
            
            # Calculate scores
            scores = evaluator.evaluate(image, current_prompt)
            
            result = {
                "prompt": current_prompt,
                "image_url": image_url,
                "aesthetic_score": scores["aesthetic_score"],
                "hpscore": scores["hpsv2_score"],
                "combined_score": scores["combined_score"],
                "timestamp": metadata["timestamp"],
                "generation_time": metadata["generation_time"]
            }
            
            current_score = result["combined_score"]
            print(f"📊 Scores - Aesthetic: {result['aesthetic_score']:.2f}, HPSv2: {result['hpscore']:.2f}, Combined: {current_score:.2f}")
            
            # Track best result
            if current_score > best_score:
                best_score = current_score
                best_result = result
                print(f"🎉 New best score: {best_score:.2f}")
            
            optimization_history.append(result)
            
            # Generate optimized prompt for next iteration (except on last iteration)
            if iteration < iterations - 1 and optimizer.enabled:
                print("🔧 Generating optimized prompt...")
                
                feedback = f"Current aesthetic score: {result['aesthetic_score']:.2f}, HPSv2 score: {result['hpscore']:.2f}"
                if iteration > 0:
                    feedback += f" (Previous best: {best_score:.2f})"
                
                optimized_prompt = optimizer.optimize(
                    original_prompt=user_prompt,
                    current_score=current_score,
                    feedback=feedback
                )
                current_prompt = optimized_prompt
                print(f"✨ Next prompt: '{current_prompt}'")
                
        except Exception as e:
            print(f"❌ Error in iteration {iteration + 1}: {str(e)}")
            result = {
                "prompt": current_prompt,
                "error": str(e),
                "combined_score": 0.0
            }
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
    
    # Save results
    results = {
        "original_prompt": user_prompt,
        "final_prompt": best_result["prompt"] if best_result else user_prompt,
        "final_result": best_result,
        "optimization_history": optimization_history,
        "best_score": best_score,
        "iterations_completed": len(optimization_history)
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"optimization_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return results


def main():
    """Main interactive function."""
    print("🎨 AI-Powered Prompt Optimization System (Simplified)")
    print("=" * 60)
    
    # Get user input
    user_input = input("Enter your initial prompt: ")
    iterations_input = input("Number of iterations (default 3): ").strip()
    
    try:
        iterations = int(iterations_input) if iterations_input else 3
    except ValueError:
        iterations = 3
        print("Invalid input, using default 3 iterations.")
    
    # Run optimization
    results = run_optimization(user_input, iterations)
    
    return results


if __name__ == "__main__":
    main()