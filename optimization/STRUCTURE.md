# Project Structure Overview

This document provides a comprehensive overview of the organized optimization system structure.

## 📁 Directory Structure

```
optimization/
├── 📄 __init__.py                 # Package initialization & convenience functions
├── 📄 prompt_optimization.py      # Main CLI interface
├── 📄 run_optimization.py         # Convenience runner script
├── 📄 README.md                  # Main documentation
├── 📄 OPTIMIZATION_GUIDE.md      # Comprehensive usage guide
├── 📄 STRUCTURE.md               # This file
├── 📄 requirements.txt           # Python dependencies
├── 📄 prompt_optimization.ipynb  # Jupyter notebook version
│
├── 📁 src/                       # Source Code
│   ├── 📄 __init__.py
│   ├── 📁 core/                  # Core Business Logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 optimization_engine.py    # Main orchestration
│   │   └── 📄 prompt_evaluator.py       # Evaluation coordination
│   ├── 📁 models/                # Model Components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 image_generator.py        # FAL AI integration
│   │   ├── 📄 evaluators.py            # Scoring models
│   │   └── 📄 dspy_optimizer.py        # DSPy optimization
│   └── 📁 utils/                 # Utility Functions
│       ├── 📄 __init__.py
│       └── 📄 utils.py           # Helper functions
│
├── 📁 config/                    # Configuration
│   ├── 📄 __init__.py
│   └── 📄 optimization_config.py # Settings & parameters
│
├── 📁 tests/                     # Test Suite
│   ├── 📄 __init__.py
│   └── 📄 test_optimization.py   # Comprehensive tests
│
├── 📁 examples/                  # Usage Examples
│   ├── 📄 __init__.py
│   └── 📄 example_usage.py       # Demo scripts
│
└── 📁 data/                      # Data Storage
    ├── 📄 README.md              # Data directory documentation
    ├── 📁 results/               # Optimization results
    ├── 📁 cache/                 # Cached evaluations
    ├── 📁 models/                # Model files
    └── 📁 exports/               # Exported reports
```

## 🎯 Design Principles

### 1. **Separation of Concerns**
- **`src/core/`**: Business logic and orchestration
- **`src/models/`**: Individual model components
- **`src/utils/`**: Shared utility functions
- **`config/`**: All configuration in one place
- **`tests/`**: Comprehensive test coverage
- **`examples/`**: Usage demonstrations
- **`data/`**: Persistent data storage

### 2. **Clean Imports**
```python
# Package-level convenience
from optimization import optimize_prompt

# Direct component access
from optimization.src.core import OptimizationEngine
from optimization.src.models import ImageGenerator
```

### 3. **Modular Architecture**
- Each component can be used independently
- Easy to test individual parts
- Simple to extend or replace components
- Clear dependency relationships

## 🚀 Usage Patterns

### Quick Start (Package Level)
```python
from optimization import optimize_prompt
results = optimize_prompt("a sunset", iterations=3)
```

### Advanced Usage (Component Level)
```python
from optimization.src.core import OptimizationEngine
from optimization.src.models import CombinedEvaluator

engine = OptimizationEngine()
evaluator = CombinedEvaluator()
```

### CLI Usage
```bash
# From optimization directory
python prompt_optimization.py

# From any directory
python optimization/run_optimization.py
```

### Testing
```bash
# Run all tests
python optimization/tests/test_optimization.py

# Run examples
python optimization/examples/example_usage.py
```

## 🔧 Development Workflow

### Adding New Features
1. **Models**: Add to `src/models/` with appropriate `__init__.py` exports
2. **Core Logic**: Extend `src/core/` components
3. **Configuration**: Update `config/optimization_config.py`
4. **Tests**: Add tests to `tests/test_optimization.py`
5. **Examples**: Add usage examples to `examples/`

### File Organization Rules
- **One class per file** in most cases
- **Related functionality grouped** in same directory
- **Clear naming conventions** (descriptive, not abbreviated)
- **Consistent import patterns** throughout the project

## 📊 Benefits of This Structure

### ✅ **Maintainability**
- Easy to locate specific functionality
- Clear separation of concerns
- Consistent organization patterns

### ✅ **Testability**
- Each component can be tested in isolation
- Clear test organization
- Easy to add new tests

### ✅ **Extensibility**
- Simple to add new models or evaluators
- Plugin-like architecture for new features
- Configuration-driven behavior

### ✅ **Usability**
- Multiple usage patterns supported
- Clear documentation and examples
- Intuitive import structure

### ✅ **Professional Standards**
- Follows Python packaging best practices
- Clean project structure
- Proper documentation organization

## 🔄 Migration from Old Structure

The old flat structure has been reorganized as follows:

| Old Location | New Location | Purpose |
|-------------|-------------|---------|
| `optimization_engine.py` | `src/core/optimization_engine.py` | Core logic |
| `prompt_evaluator.py` | `src/core/prompt_evaluator.py` | Core logic |
| `image_generator.py` | `src/models/image_generator.py` | Model component |
| `evaluators.py` | `src/models/evaluators.py` | Model component |
| `dspy_optimizer.py` | `src/models/dspy_optimizer.py` | Model component |
| `utils.py` | `src/utils/utils.py` | Utilities |
| `optimization_config.py` | `config/optimization_config.py` | Configuration |
| `test_optimization.py` | `tests/test_optimization.py` | Tests |
| `example_usage.py` | `examples/example_usage.py` | Examples |

All import statements have been updated accordingly, and the package maintains backward compatibility through the main `__init__.py` file.