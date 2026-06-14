from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key="Add yours openrouter Api key",
    base_url="https://openrouter.ai/api/v1"
)

# Chat memory
chat_history = [
    {
        "role": "system",
        "content": """
        You are CampusBot, an AI educational assistant.

        Rules:
        - Give short and clear answers.
        - Use bullet points whenever possible.
        - Do not write long paragraphs.
        - Keep responses under 100 words.
        - Answer like a college student assistant.

        Help students with:
        - Admissions
        - Courses
        - Exams
        - Library information
        - Placements
        - Educational guidance

        This project supports SDG 4: Quality Education.
        """
    }
]

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]

        # Save user message
        chat_history.append({
            "role": "user",
            "content": user_message
        })

      
        if len(chat_history) > 20:
            chat_history[:] = [chat_history[0]] + chat_history[-19:]

        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=chat_history
        )

        reply = response.choices[0].message.content

        # Save bot reply
        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)
