"""
Configuration settings for the prompt optimization system.
"""

# Default optimization settings
DEFAULT_ITERATIONS = 5
DEFAULT_MODEL = "fal-ai/imagen4/preview"

# Scoring weights (should sum to 1.0)
AESTHETIC_WEIGHT = 0.5
HPSV2_WEIGHT = 0.5

# DSPy optimization settings
DSPY_MODEL = "solar-pro2"  # Can be changed to gpt-4 for better optimization
DSPY_MAX_TOKENS = 1000

IMAGE_SIZE = "square_hd"
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 7.5

# Optimization prompt template
OPTIMIZATION_TEMPLATE = """
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

# File naming patterns
RESULTS_FILENAME_PATTERN = "optimization_results_{timestamp}.json"
IMAGE_FILENAME_PATTERN = "{model}_{timestamp}.jpg"

# Logging settings
LOG_LEVEL = "INFO"
SAVE_INTERMEDIATE_RESULTS = True
