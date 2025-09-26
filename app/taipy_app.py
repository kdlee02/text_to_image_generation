import requests
from taipy.gui import Gui, Markdown
import json

# State variables
prompt = ""
aspect_ratio = "1:1"
generated_image_url = ""
loading = False
history_loading = False
image_history = []
error_message = ""
success_message = ""

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

def generate_image(state):
    """Generate image by calling FastAPI backend"""
    if not state.prompt.strip():
        state.error_message = "⚠️ Please enter a prompt to generate an image"
        state.success_message = ""
        return
    
    state.loading = True
    state.error_message = ""
    state.success_message = ""
    state.generated_image_url = ""
    
    try:
        # Call your existing FastAPI endpoint
        response = requests.post(
            f"{FASTAPI_URL}/api/generate_image",
            json={"user_input": state.prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            state.generated_image_url = result.get("image_url", "")
            state.success_message = "✅ Image generated successfully!"
            state.error_message = ""
        else:
            state.error_message = f"❌ Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        state.error_message = f"🔌 Connection error: Make sure FastAPI is running on port 8000. {str(e)}"
    except Exception as e:
        state.error_message = f"💥 Unexpected error: {str(e)}"
    finally:
        state.loading = False

def load_history(state):
    """Load image history from FastAPI backend"""
    state.history_loading = True
    state.error_message = ""
    
    try:
        response = requests.get(f"{FASTAPI_URL}/api/get_images", timeout=30)
        
        if response.status_code == 200:
            history_data = response.json()
            state.image_history = history_data
            state.success_message = f"📚 Loaded {len(history_data)} images from history"
        else:
            state.error_message = f"❌ Error loading history: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        state.error_message = f"🔌 Connection error: {str(e)}"
    except Exception as e:
        state.error_message = f"💥 Unexpected error: {str(e)}"
    finally:
        state.history_loading = False

def clear_form(state):
    """Clear the form"""
    state.prompt = ""
    state.generated_image_url = ""
    state.error_message = ""
    state.success_message = ""

def on_prompt_change(state):
    """Handle prompt input changes"""
    # Clear messages when user starts typing
    if state.prompt:
        state.error_message = ""

# Enhanced page layout with better input handling
page = """
# 🎨 AI Event Banner Generator

## ✨ Create Your Banner

**📝 Event Description**
<|{prompt}|input|label=Describe your event in detail|placeholder=e.g., "Luxury Tech Conference 2025 with modern design and blue theme"|>

**📐 Aspect Ratio**
<|{aspect_ratio}|selector|lov=['1:1', '16:9', '4:3', '3:4']|dropdown|label=Choose your banner format|>

<|Generate Image|button|on_action=generate_image|active={not loading and len(prompt.strip()) > 0}|>
<|Clear Form|button|on_action=clear_form|>

<|{error_message}|text|active={len(error_message) > 0}|>
<|{success_message}|text|active={len(success_message) > 0}|>
<|🎨 Generating your amazing banner... Please wait!|text|active={loading}|>

<|{generated_image_url}|image|active={len(generated_image_url) > 0}|width=600px|>

---

## 📚 Image History

<|Load Previous Images|button|on_action=load_history|active={not history_loading}|>
<|📚 Loading your image history...|text|active={history_loading}|>

<|{image_history}|table|active={len(image_history) > 0}|>
"""

if __name__ == "__main__":
    # Create and run the Taipy GUI
    gui = Gui(page)
    
    print("🚀 Starting Taipy frontend...")
    print("📡 Make sure your FastAPI backend is running on http://localhost:8000")
    print("🌐 Taipy will be available at http://localhost:5000")
    
    gui.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        run_browser=True
    )