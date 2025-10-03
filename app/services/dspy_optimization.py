import dspy
import os
from PIL import Image
from io import BytesIO
import requests
import fal_client
from dotenv import load_dotenv
import base64
import requests
from models.image_manager import ImageManager
load_dotenv()


lm = dspy.LM(model="gemini/gemini-2.5-pro",api_key=os.environ["GEMINI_API_KEY"])
dspy.settings.configure(lm=lm)

addingimage = ImageManager()

def generate_image(prompt):
    request_id = fal_client.submit(
        "fal-ai/imagen4/preview",
        arguments={
            "prompt": prompt
        },
    ).request_id

    result = fal_client.result("fal-ai/imagen4/preview", request_id)
    url = result["images"][0]["url"]
    addingimage.add_image(prompt, result["images"][0])
    return dspy.Image.from_url(url), url

def dspy_opt(user_input):

    initial_prompt = user_input
    current_prompt = initial_prompt

    check_and_revise_prompt = dspy.ChainOfThought("""
    desired_prompt: str, 
    current_image: dspy.Image, 
    current_prompt: str,
    previous_attempts: str -> 
    reasoning: str,

    overall_prompt_match: bool,
    subject_match: bool,
    art_type_match: bool,
    art_style_match: bool,
    art_movement_match: bool,

    has_conflicting_elements: bool,
    conflict_description: str,

    overall_prompt_match_feedback: str,
    subject_feedback: str,
    art_type_feedback: str,
    art_style_feedback: str,
    art_movement_feedback: str,
    revised_prompt: str
    """)

    history = []

    url = ''
    
    for i in range(5):
        current_image, url = generate_image(current_prompt)
        #display_image(current_image)
        #print(f'current prompt: {current_prompt}')
        # Format history for context
        history_str = "\n".join([
        f"Attempt {idx+1}: {h['prompt']}\n" +
        f"  Subject: {h['detailed_feedback']['subject']}\n" +
        f"  Art Type: {h['detailed_feedback']['art_type']}\n" +
        f"  Style: {h['detailed_feedback']['style']}\n" +
        f"  Art Movement: {h['detailed_feedback']['art_movement']}\n" +
        f"  Conflicts: {h['detailed_feedback']['conflicts']}"
        for idx, h in enumerate(history)
    ]) if history else "No previous attempts"

        result = check_and_revise_prompt(
            desired_prompt=initial_prompt, 
            current_image=current_image, 
            current_prompt=current_prompt,
            previous_attempts=history_str
        )
        # Store this attempt
        history.append({
            'prompt': current_prompt,
            'detailed_feedback': {
            'subject': result.subject_feedback,
            'art_type': result.art_type_feedback,
            'style': result.art_style_feedback,
            'art_movement': result.art_movement_feedback,
            'conflicts': result.conflict_description
        }
        })
        
        if result.subject_match and result.art_type_match and result.art_style_match and result.overall_prompt_match and not result.has_conflicting_elements and result.art_movement_match:
            print("")
            print("✓ All components match perfectly!")
            print(f"Subject - {result.subject_feedback}")
            print(f"Art Type - {result.art_type_feedback}")
            print(f"Art Style - {result.art_style_feedback}")
            print(f"Art Movement - {result.art_movement_feedback}")
            print(f"Overall Prompt - {result.overall_prompt_match_feedback}")
            print(f"Confliction:- {result.conflict_description}")
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
        else:
            print(f"Subject Match: {'✓' if result.subject_match else '✗'} - {result.subject_feedback}")
            print(f"Art Type Match: {'✓' if result.art_type_match else '✗'} - {result.art_type_feedback}")
            print(f"Art Movement Match: {'✓' if result.art_movement_match else '✗'} - {result.art_movement_feedback}")
            print(f"Art Style Match: {'✓' if result.art_style_match else '✗'} - {result.art_style_feedback}")
            print(f"Overall Prompt Match: {'✓' if result.overall_prompt_match else '✗'} - {result.overall_prompt_match_feedback}")
            print(f"Confliction: {'✓' if not result.has_conflicting_elements else '✗'} - {result.conflict_description}")
            print(f"\nRevised prompt: {result.revised_prompt}")
            current_prompt = result.revised_prompt
            
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")