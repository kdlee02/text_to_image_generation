# Prompt Optimization Guide

This guide explains how to use the AI-powered prompt optimization system to automatically improve your image generation prompts.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys in `.env`:**
   ```bash
   FAL_KEY=your-fal-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

3. **Run optimization:**
   ```bash
   python prompt_optimization.py
   ```

## How It Works

The optimization system uses a sophisticated approach combining:

- **DSPy Framework**: For intelligent prompt reasoning and optimization
- **Aesthetic Evaluation**: Using aesthetic-predictor-v2-5 model
- **Human Preference Scoring**: Using HPSv2 for alignment with human preferences
- **Iterative Improvement**: Multiple rounds of refinement

### The Process

1. **Initial Generation**: Creates image from your original prompt
2. **Score Evaluation**: Calculates aesthetic and HPSv2 scores
3. **Prompt Analysis**: DSPy analyzes what could be improved
4. **Optimization**: Generates an enhanced version of the prompt
5. **Repeat**: Continues for 5 iterations (configurable)
6. **Best Selection**: Returns the highest-scoring result

## Usage Examples

### Basic Command Line Usage

```bash
python prompt_optimization.py
# Enter your initial prompt: a sunset over mountains
```

### Programmatic Usage

```python
from prompt_optimization import optimize_prompt_iteratively, display_optimization_results

# Basic optimization
results = optimize_prompt_iteratively("a cat in a garden")
print(f"Best prompt: {results['final_prompt']}")
print(f"Score improvement: {results['best_score']:.2f}")

# Custom iterations
results = optimize_prompt_iteratively("abstract art", iterations=3)

# Display detailed results
display_optimization_results(results)
```

### Batch Optimization

```python
prompts = [
    "a robot in space",
    "a medieval castle",
    "modern architecture"
]

for prompt in prompts:
    results = optimize_prompt_iteratively(prompt)
    print(f"Original: {prompt}")
    print(f"Optimized: {results['final_prompt']}")
    print(f"Score: {results['best_score']:.2f}")
    print("-" * 50)
```

## Configuration

Edit `optimization_config.py` to customize:

### Basic Settings
```python
DEFAULT_ITERATIONS = 5          # Number of optimization rounds
AESTHETIC_WEIGHT = 0.5          # Weight for aesthetic score
HPSV2_WEIGHT = 0.5             # Weight for HPSv2 score
```

### Model Settings
```python
DEFAULT_MODEL = "fal-ai/imagen4/preview"  # Image generation model
DSPY_MODEL = "gpt-3.5-turbo"             # DSPy optimization model
```

### Image Generation Parameters
```python
IMAGE_SIZE = "square_hd"        # Image dimensions
NUM_INFERENCE_STEPS = 50        # Generation quality vs speed
GUIDANCE_SCALE = 7.5           # Prompt adherence strength
```

## Understanding the Scores

### Aesthetic Score
- Range: Typically 0-10
- Measures: Visual appeal, composition, color harmony
- Higher is better

### HPSv2 Score  
- Range: Typically 0-10
- Measures: Alignment with human preferences
- Higher is better

### Combined Score
- Weighted average of both scores
- Used for optimization decisions
- Configurable weights in `optimization_config.py`

## Optimization Strategies

The system applies several enhancement techniques:

### 1. Visual Detail Enhancement
- **Before**: "a cat"
- **After**: "a fluffy orange tabby cat with bright green eyes"

### 2. Style and Quality Descriptors
- **Before**: "a landscape"
- **After**: "a breathtaking landscape, highly detailed, professional photography"

### 3. Lighting and Composition
- **Before**: "a portrait"
- **After**: "a portrait with dramatic lighting, perfect composition, golden hour"

### 4. Technical Quality Terms
- **Before**: "digital art"
- **After**: "digital art, 8k resolution, trending on artstation, masterpiece"

## Tips for Best Results

### 1. Start with Clear Concepts
```python
# Good starting prompts
"a sunset over mountains"
"a robot in a futuristic city"
"abstract geometric patterns"

# Less ideal starting prompts
"something cool"
"art"
"picture"
```

### 2. Monitor Score Improvements
```python
results = optimize_prompt_iteratively("your prompt")
history = results['optimization_history']

for i, result in enumerate(history):
    print(f"Iteration {i+1}: {result['combined_score']:.2f}")
```

### 3. Experiment with Different Models
```python
# In optimization_config.py, try different models:
DSPY_MODEL = "gpt-4"  # Better optimization but more expensive
DSPY_MODEL = "gpt-3.5-turbo"  # Good balance of quality and cost
```

### 4. Adjust Scoring Weights
```python
# For more artistic images
AESTHETIC_WEIGHT = 0.7
HPSV2_WEIGHT = 0.3

# For more human-preferred images
AESTHETIC_WEIGHT = 0.3
HPSV2_WEIGHT = 0.7
```

## Troubleshooting

### Common Issues

1. **"DSPy not available" error**
   - Check OPENAI_API_KEY in .env file
   - Verify OpenAI API key is valid
   - Ensure dspy-ai is installed: `pip install dspy-ai`

2. **"Failed to generate image" error**
   - Check FAL_KEY in .env file
   - Verify FAL AI API key is valid
   - Check internet connection

3. **Low scores consistently**
   - Try different starting prompts
   - Adjust scoring weights in config
   - Increase number of iterations

4. **CUDA/GPU errors**
   - Aesthetic model requires GPU
   - Install PyTorch with CUDA support
   - Or modify code to use CPU (slower)

### Performance Tips

1. **GPU Memory**: The aesthetic model uses GPU memory. Close other GPU applications if needed.

2. **API Rate Limits**: Both OpenAI and FAL AI have rate limits. The system includes delays between requests.

3. **Cost Management**: Each iteration costs API credits. Monitor usage in your dashboards.

## Advanced Usage

### Custom Evaluation Metrics

```python
def custom_evaluate_prompt(prompt: str) -> Dict:
    """Custom evaluation function."""
    generator = ImageGenerator()
    result = generator.evaluate_prompt(prompt)
    
    # Add custom scoring logic
    custom_score = your_custom_scoring_function(result)
    result['custom_score'] = custom_score
    
    return result
```

### Integration with Other Tools

```python
# Save results to database
import sqlite3

def save_to_database(results):
    conn = sqlite3.connect('optimization_results.db')
    # Save results...
    conn.close()

# Use with existing image generation pipeline
def enhanced_generation_pipeline(prompt):
    # Optimize first
    results = optimize_prompt_iteratively(prompt)
    optimized_prompt = results['final_prompt']
    
    # Then generate with your existing system
    return your_image_generator(optimized_prompt)
```

## File Outputs

The system creates several files:

- `optimization_results_TIMESTAMP.json`: Detailed results
- Downloaded images in temp directories
- Console logs with progress information

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Verify API keys and dependencies
4. Check the example scripts for reference patterns