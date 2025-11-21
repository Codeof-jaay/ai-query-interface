import re
from google import genai
import os
from dotenv import load_dotenv


# LOAD ENVIRONMENT VARIABLES
load_dotenv()  # loads .env from current directory

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Make sure it is set in your .env file.")


# 1. BASIC PREPROCESSING FUNCTION
def preprocess_question(question: str) -> str:
    # lowercase
    question = question.lower()

    # remove punctuation
    question = re.sub(r'[^\w\s]', '', question)

    # tokenization (simple split)
    tokens = question.split()

    # join back as processed string
    processed = " ".join(tokens)

    return processed



# 2. PROMPT CONSTRUCTION

def build_prompt(original_question, processed_question):
    prompt = f"""
You are an advanced question-answering AI.

The user asked:
"{original_question}"

After preprocessing, the question becomes:
"{processed_question}"

Please give a clear, direct, helpful answer.
"""
    return prompt



# 3. GOOGLE GENAI CLIENT SETUP

def get_gemini_client():
    # Make sure $GOOGLE_API_KEY is set in your environment or .env
    return genai.Client(api_key=None)  # Automatically picks from env



# 4. MAIN CLI LOOP
def main():
    print("=== LLM Q&A CLI — Google Gemini ===")
    print("Type 'exit' to quit.\n")

    client = get_gemini_client()

    while True:
        user_q = input("Enter your question: ")

        if user_q.lower() == "exit":
            print("Exiting program. Goodbye!")
            break

        # Preprocess
        processed = preprocess_question(user_q)
        print(f"[Processed Question]: {processed}")

        # Build final prompt
        final_prompt = build_prompt(user_q, processed)

        # Send to Gemini LLM
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=final_prompt
            )
            answer = response.text
        except Exception as e:
            answer = f"Error contacting Gemini API: {e}"

        print("\n=== LLM Answer ===")
        print(answer)
        print("\n-----------------------------\n")


if __name__ == "__main__":
    main()
