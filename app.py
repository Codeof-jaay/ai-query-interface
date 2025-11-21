from flask import Flask, render_template, request, redirect, url_for, jsonify
from google import genai
from flask_cors import CORS  # allows frontend to connect from a different port
import markdown
import os

# Try to import python-dotenv's loader; if unavailable, provide a small fallback
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(path='.env'):
        """Fallback .env loader: reads KEY=VALUE lines into os.environ if present."""
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    v = v.strip().strip('"').strip("'")
                    os.environ.setdefault(k.strip(), v)


load_dotenv()  # Load environment variables from .env file (or fallback)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Initialize genai client if key is present; otherwise provide a safe stub client
def _make_stub_client():
    class _Models:
        def generate_content(self, model=None, contents=None, **kwargs):
            class _R:
                pass
            r = _R()
            r.text = (
                "[stub] GEMINI_API_KEY not configured. "
                "Install/configure the key to call the real API.\n\n"
                f"Prompt received:\n{contents}"
            )
            return r

    class _Client:
        def __init__(self):
            self.models = _Models()

    return _Client()

try:
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)  # real client
    else:
        client = _make_stub_client()
except Exception:
    # If genai import or client creation fails for any reason, fall back to stub
    client = _make_stub_client()

# Ensure the installed 'dotenv' module (if present but not python-dotenv) exposes
# the minimal API Flask expects (find_dotenv and load_dotenv). This avoids
# AttributeError when Flask's CLI tries to call dotenv.find_dotenv.
try:
    import importlib, sys
    dotenv_mod = importlib.import_module('dotenv') if 'dotenv' in sys.modules or importlib.util.find_spec('dotenv') else None
    if dotenv_mod is not None:
        # provide find_dotenv if missing
        if not hasattr(dotenv_mod, 'find_dotenv'):
            def _find_dotenv(default_name='.env', usecwd=True):
                return default_name if os.path.exists(default_name) else ''
            setattr(dotenv_mod, 'find_dotenv', _find_dotenv)
        # provide load_dotenv if missing
        if not hasattr(dotenv_mod, 'load_dotenv'):
            setattr(dotenv_mod, 'load_dotenv', load_dotenv)
        # provide dotenv_values if missing
        if not hasattr(dotenv_mod, 'dotenv_values'):
            def _dotenv_values(path, encoding='utf-8'):
                result = {}
                if not path or not os.path.exists(path):
                    return result
                with open(path, 'r', encoding=encoding) as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '=' in line:
                            k, v = line.split('=', 1)
                            v = v.strip().strip('"').strip("'")
                            result[k.strip()] = v
                return result
            setattr(dotenv_mod, 'dotenv_values', _dotenv_values)
except Exception:
    pass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    original = ''
    output_text = ''
    response = None
    if request.method == 'POST':
        original = request.form.get('input_text', '')
        prompt = f"Answer my question Respond using clean markdown formatting.: {original}"
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            markdown_text = response.text

            # Convert markdown → HTML
            output_text = markdown.markdown(
                markdown_text,
                extensions=["fenced_code", "tables", "nl2br"]
            )
        except Exception as e:
            # keep response as None and show the error message in template
            response = type('E', (), {'text': str(e)})()

    return render_template('index.html',
                           input_text=original,
                           output_text=output_text)

if __name__ == '__main__':
    # Use PORT env var when present to avoid collisions with default 5000.
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5001)))
    app.run(debug=True, port=port)