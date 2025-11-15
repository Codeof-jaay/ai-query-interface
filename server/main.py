from flask import Flask, request, jsonify
from google import genai
from flask_cors import CORS  # allows frontend to connect from a different port
from image_routes import image_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
  # enable CORS for all routes
app.register_blueprint(image_bp)

@app.route("/add", methods=["POST"])

def add_numbers():
    data = request.get_json()
    try:
        var1 = data.get("num1", 0)
        var2 = data.get("num2", 0)
        var3 = data.get("num3", 0)

        prompt = f"Make only one sentence with the words {var1}, {var2} and {var3}"
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
        )

        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400 

if __name__ == "__main__":
    app.run(debug=True, port=5000)
