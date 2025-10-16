from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()
print("API Key Loaded:", os.getenv("OPENAI_API_KEY")[:10], "...")


app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Chat logic ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # Generate AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can use gpt-4o for more detail
            messages=[
                {"role": "system", "content": (
                    "You are a cybersecurity incident response assistant. "
                    "Your role is to help users analyze, respond to, and document security incidents. "
                    "Respond clearly and professionally with practical steps and reasoning."
                )},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=300
        )

        ai_reply = response.choices[0].message.content.strip()

        return jsonify({"response": ai_reply, "category": "AI Response"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "⚠️ Error: Unable to reach AI service.", "category": "System Error"})

if __name__ == "__main__":
    app.run(debug=True)
