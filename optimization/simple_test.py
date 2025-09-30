#!/usr/bin/env python3
"""
Simple test script to verify the optimization system works.
"""

import sys
import os
from pathlib import Path

# Add the optimization directory to Python path
optimization_dir = Path(__file__).parent
sys.path.insert(0, str(optimization_dir))

# Test basic imports
try:
    print("Testing basic imports...")
    
    # Test config import
    from config.optimization_config import DEFAULT_MODEL, AESTHETIC_WEIGHT, HPSV2_WEIGHT
    print(f"✅ Config loaded: {DEFAULT_MODEL}")
    
    # Test FAL client
    import fal_client
    print("✅ FAL client imported")
    
    # Test dotenv
    from dotenv import load_dotenv
    root_dir = optimization_dir.parent.parent
    env_path = root_dir / '.env'
    load_dotenv(env_path)
    print("✅ Environment loaded")
    
    # Test API keys
    fal_key = os.getenv('FAL_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    print(f"✅ FAL Key: {'Found' if fal_key else 'Missing'}")
    print(f"✅ OpenAI Key: {'Found' if openai_key else 'Missing'}")
    
    # Test a simple image generation
    if fal_key:
        print("\n🎯 Testing image generation...")
        response = fal_client.run(
            "fal-ai/imagen4/preview",
            arguments={
                "prompt": "a simple test image of a cat",
                "image_size": "square_hd",
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        )
        
        if response and "images" in response:
            image_url = response["images"][0]["url"]
            print(f"✅ Image generated: {image_url}")
        else:
            print("❌ No image in response")
    else:
        print("⚠️ Skipping image generation - no FAL key")
    
    print("\n🎉 All basic tests passed!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()