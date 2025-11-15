from flask import Flask, render_template, request, redirect, url_for, jsonify
from google import genai
from flask_cors import CORS  # allows frontend to connect from a different port
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # or service account creds

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def give_response():
    data = request.get_json()
    try:
        Query = data.get("num1", 0)

        prompt = f"Answer my question: {Query}"
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
        )

        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400 

def index():
    output = None
    original = None
    if request.method == 'POST':
        original = request.form.get('input_text', '')
        output = give_response(original)
    return render_template('index.html', input_text=original or '', output_text=output)


if __name__ == '__main__':
    app.run(debug=True)