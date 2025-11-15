# image_routes.py
from flask import Blueprint, request, jsonify
import os
from imagen_handler import generate_image_from_prompt, edit_image_with_prompt

image_bp = Blueprint('image_bp', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@image_bp.route('/upload_and_generate', methods=['POST'])
def upload_and_generate():
    """
    Receives image and text prompt, sends to Imagen for generation/editing.
    """
    prompt = request.form.get('prompt')
    image_file = request.files.get('image')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    if image_file:
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)
        generated = edit_image_with_prompt(image_path, prompt)
    else:
        generated = generate_image_from_prompt(prompt)

    if not generated:
        return jsonify({'error': 'Image generation failed'}), 500

    # Return the base64 image(s)
    return jsonify({
        'message': 'Image generated successfully',
        'images': generated
    })
