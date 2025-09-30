# Modular Prompt Optimization System

A sophisticated, modular system for optimizing AI image generation prompts using DSPy, aesthetic evaluation, and human preference scoring.

## 🏗️ Architecture

The system is built with a clean, organized architecture following Python best practices:

```
optimization/
├── __init__.py                 # Package initialization and convenience functions
├── prompt_optimization.py      # Main CLI interface
├── README.md                  # This documentation
├── OPTIMIZATION_GUIDE.md      # Comprehensive usage guide
├── requirements.txt           # Python dependencies
├── src/                       # Source code
│   ├── core/                  # Core optimization logic2
│   │   ├── optimization_engine.py    # Main orchestration
│   │   └── prompt_evaluator.py       # Evaluation coordinator
│   ├── models/                # Model components
│   │   ├── image_generator.py        # FAL AI integration
│   │   ├── evaluators.py            # Scoring models
│   │   └── dspy_optimizer.py        # DSPy optimization
│   └── utils/                 # Utility functions
│       └── utils.py           # Helper functions
├── config/                    # Configuration
│   └── optimization_config.py # Settings and parameters
├── tests/                     # Test suite
│   └── test_optimization.py   # Comprehensive tests
├── examples/                  # Usage examples
│   └── example_usage.py       # Demo scripts
└── data/                      # Data storage (results, cache)
```

## 🚀 Quick Start

### Basic Usage

```python
from optimization import optimize_prompt

# Simple optimization
results = optimize_prompt("a sunset over mountains", iterations=5)
print(f"Best prompt: {results['final_prompt']}")
print(f"Score: {results['best_score']:.2f}")
```

### Advanced Usage

```python
from optimization import OptimizationEngine, display_optimization_results

# Create engine with custom settings
engine = OptimizationEngine()

# Run optimization
results = engine.optimize_iteratively("a cat in a garden", iterations=3)

# Display detailed results
display_optimization_results(results)
```

### Command Line Interface

```bash
python prompt_optimization.py
# Enter your initial prompt: a beautiful landscape
# Number of iterations (default 5): 3
```

## 📦 Modules

### 1. Core Components (`src/core/`)

**OptimizationEngine** - Main orchestrator that coordinates the entire optimization process.

```python
from src.core.optimization_engine import OptimizationEngine

engine = OptimizationEngine(api_key="your-fal-key")  # Optional API key
results = engine.optimize_iteratively("your prompt", iterations=5)
```

**PromptEvaluator** - Handles prompt evaluation by combining image generation and scoring.

```python
from src.core.prompt_evaluator import PromptEvaluator

evaluator = PromptEvaluator()
result = evaluator.evaluate_prompt("a mountain landscape")
print(f"Combined score: {result['combined_score']:.2f}")
```

### 2. Model Components (`src/models/`)

**ImageGenerator** - Manages FAL AI image generation with configurable parameters.

```python
from src.models.image_generator import ImageGenerator

generator = ImageGenerator()
image_url, metadata = generator.generate_image("a sunset")
image = generator.download_image(image_url)
```

**Evaluators** - Provides aesthetic and human preference scoring capabilities.

```python
from src.models.evaluators import CombinedEvaluator

evaluator = CombinedEvaluator()
scores = evaluator.evaluate(image, prompt)
print(f"Aesthetic: {scores['aesthetic_score']:.2f}")
print(f"HPSv2: {scores['hpsv2_score']:.2f}")
```

**DSPyOptimizer** - Handles DSPy configuration and prompt optimization logic.

```python
from src.models.dspy_optimizer import DSPyManager

dspy_manager = DSPyManager()
if dspy_manager.enabled:
    optimized = dspy_manager.optimize_prompt(
        original_prompt="a cat",
        current_score=6.5,
        feedback="Add more visual details"
    )
```

### 3. Utilities (`src/utils/`)

**Utils** - Utility functions for result display, file operations, and comparisons.

```python
from src.utils.utils import display_optimization_results, save_results_to_file

# Display results
display_optimization_results(results)

# Save to file
filename = save_results_to_file(results)
print(f"Saved to: {filename}")
```

## ⚙️ Configuration

Edit `config/optimization_config.py` to customize system behavior:

```python
# Optimization settings
DEFAULT_ITERATIONS = 5
AESTHETIC_WEIGHT = 0.5
HPSV2_WEIGHT = 0.5

# Model settings
DSPY_MODEL = "gpt-3.5-turbo"
DEFAULT_MODEL = "fal-ai/imagen4/preview"

# Image generation parameters
IMAGE_SIZE = "square_hd"
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 7.5
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests/test_optimization.py
```

The test suite includes:
- Package import tests
- Individual component tests
- Complete optimization workflow tests

## 📚 Examples

Run the example script to see various usage patterns:

```bash
python examples/example_usage.py
```

Examples include:
- Basic optimization
- Single prompt evaluation
- Batch optimization
- Custom configuration usage

## 🔧 Extending the System

### Adding New Evaluators

Create a new evaluator in `src/models/evaluators.py`:

```python
class CustomEvaluator:
    def calculate_score(self, image: Image.Image, prompt: str) -> float:
        # Your custom scoring logic
        return score
```

### Adding New Optimization Strategies

Extend the DSPy optimizer in `src/models/dspy_optimizer.py`:

```python
class AdvancedPromptOptimizer(dspy.Module):
    def __init__(self):
        super().__init__()
        # Your custom DSPy signature and modules
```

### Custom Image Generation Models

Modify `src/models/image_generator.py` to support new models:

```python
def generate_image(self, prompt: str, model: str = "your-custom-model"):
    # Custom generation logic
```

## 🐛 Troubleshooting

### Common Issues

1. **"DSPy not available" error**
   - Check `OPENAI_API_KEY` in your environment
   - Verify the API key is valid
   - Ensure `dspy-ai` is installed

2. **"Failed to generate image" error**
   - Check `FAL_KEY` in your environment
   - Verify the FAL AI API key is valid
   - Check internet connectivity

3. **CUDA/GPU errors**
   - Ensure PyTorch with CUDA support is installed
   - Check GPU memory availability
   - Consider using CPU mode (modify evaluators.py)

### Debug Mode

Enable detailed logging by modifying `config/optimization_config.py`:

```python
LOG_LEVEL = "DEBUG"
SAVE_INTERMEDIATE_RESULTS = True
```

## 📈 Performance Tips

1. **GPU Memory**: The aesthetic model requires GPU memory. Close other GPU applications if needed.

2. **API Rate Limits**: Both OpenAI and FAL AI have rate limits. The system includes appropriate delays.

3. **Batch Processing**: Use the batch optimization examples for processing multiple prompts efficiently.

4. **Caching**: Consider implementing result caching for repeated evaluations.

## 🤝 Contributing

To contribute to the system:

1. Follow the modular architecture
2. Add tests for new functionality
3. Update configuration as needed
4. Document new features

## 📄 License

This project is part of the larger prompt optimization system. See the main project for license details.

## 🔗 Related Files

- `../requirements.txt` - Python dependencies
- `../.env.example` - Environment variable template
- `../OPTIMIZATION_GUIDE.md` - Comprehensive usage guide