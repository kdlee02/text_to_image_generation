#!/usr/bin/env python3
"""
Test script for the modular prompt optimization system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.optimization_engine import OptimizationEngine
from src.utils.utils import display_optimization_results


def test_individual_components():
    """Test individual components of the system."""
    print("🔧 Testing Individual Components")
    print("=" * 40)
    
    try:
        # Test image generator
        from src.models.image_generator import ImageGenerator
        generator = ImageGenerator()
        print("✅ ImageGenerator initialized successfully")
        
        # Test evaluators
        from src.models.evaluators import CombinedEvaluator
        evaluator = CombinedEvaluator()
        print("✅ CombinedEvaluator initialized successfully")
        
        # Test DSPy manager
        from src.models.dspy_optimizer import DSPyManager
        dspy_manager = DSPyManager()
        print(f"✅ DSPyManager initialized (enabled: {dspy_manager.enabled})")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {str(e)}")
        return False


def test_optimization():
    """Test the complete optimization system."""
    
    # Test prompt
    test_prompt = "a beautiful sunset over mountains"
    
    print("\n🧪 Testing Complete Optimization System")
    print("=" * 50)
    print(f"Test prompt: {test_prompt}")
    
    try:
        # Initialize optimization engine
        engine = OptimizationEngine()
        
        # Run optimization with fewer iterations for testing
        results = engine.optimize_iteratively(test_prompt, iterations=2)
        
        # Display results
        display_optimization_results(results)
        
        print("\n✅ Optimization test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Optimization test failed: {str(e)}")
        return False


def test_package_import():
    """Test importing the optimization package."""
    print("📦 Testing Package Import")
    print("=" * 30)
    
    try:
        # Test package-level import
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import optimization
        
        # Test convenience function
        print("✅ Package imported successfully")
        print(f"✅ Package version: {optimization.__version__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Package import failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("🚀 Running Modular Optimization System Tests")
    print("=" * 60)
    
    tests = [
        ("Package Import", test_package_import),
        ("Individual Components", test_individual_components),
        ("Complete Optimization", test_optimization)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("🏆 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()