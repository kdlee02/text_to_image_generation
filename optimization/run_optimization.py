#!/usr/bin/env python3
"""
Convenience script to run the optimization system from any directory.
"""

import sys
import os

# Add the optimization directory to the Python path
optimization_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, optimization_dir)

# Import and run the main optimization function
from prompt_optimization import main

if __name__ == "__main__":
    main()