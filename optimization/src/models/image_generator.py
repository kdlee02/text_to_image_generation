"""
Image generation module using FAL AI.
"""

import fal_client
import os
import requests
import time
from datetime import datetime
from typing import Dict, Tuple
from PIL import Image
import tempfile
from ...config.optimization_config import DEFAULT_MODEL


class ImageGenerator:
    """Handles image generation using FAL AI."""

    def __init__(self, api_key: str = None):
        """Initialize the FAL AI image generator."""
        if api_key:
            os.environ['FAL_KEY'] = api_key
        elif not os.getenv('FAL_KEY'):
            raise ValueError("API key required. Set FAL_KEY environment variable or provide api_key parameter.")

    def generate_image(self, prompt: str, model: str = DEFAULT_MODEL) -> Tuple[str, Dict]:
        """Generate image using FAL AI."""
        start_time = time.time()

        try:
            response = fal_client.run(
                model,
                arguments={
                    "prompt": prompt
                }
            )

            end_time = time.time()

            if response and "images" in response and len(response["images"]) > 0:
                image_url = response["images"][0]["url"]
                metadata = {
                    "model": model,
                    "prompt": prompt,
                    "timestamp": datetime.now().isoformat(),
                    "generation_time": end_time - start_time,
                    "response": response
                }
                return image_url, metadata
            else:
                raise Exception("No image generated in response")

        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")

    def download_image(self, url: str) -> Image.Image:
        """Download image from URL and return PIL Image."""
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name

            image = Image.open(tmp_path).convert("RGB")
            os.unlink(tmp_path)

            return image

        except Exception as e:
            raise Exception(f"Error downloading image: {str(e)}")