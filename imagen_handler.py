# google_imagen.py
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Generative AI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # or service account creds

def generate_image_from_prompt(prompt):
    
    #Generates an image using Google's Imagen model.
    try:
        response = client.models.generate_images(
            model="gemini-2.0-flash",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images= 1,
    )
        )
        # Return base64 image(s)
        return [img.image_base64 for img in response.generated_images]

    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def edit_image_with_prompt(image_path, prompt):
    #Optionally edit or transform a provided image using Imagen.
    try:
        response = client.models.edit_image(
            model="gemini-2.0-flash",
            prompt=prompt,
            image=open(image_path, "rb").read(),
            config=types.GenerateImagesConfig(
                number_of_images= 1,
    )
        )
        return [img.image_base64 for img in response.edited_images]

    except Exception as e:
        print(f"Error editing image: {e}")
        return None
