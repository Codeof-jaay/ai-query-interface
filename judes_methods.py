# image_routes.py
from flask import Blueprint, request, jsonify
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
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # or service account creds

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


def give_response(Query):
    prompt = f"Answer my question: {Query}"
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
    )

    return response.text
