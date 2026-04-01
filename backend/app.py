from flask import Flask,render_template,request,jsonify
import os
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)
conversation_memory = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("user_input_field_name")
        session_id = data.get("session_id", "default")

        # get history
        history = conversation_memory.get(session_id, [])

        # add user message
        history.append({
            "role": "user",
            "content": user_input
        })

        # call AI with FULL history
        response = client.responses.create(
            model="gpt-4o-mini",
            input=history
        )

        reply = response.output_text

        # add AI reply to history
        history.append({
            "role": "assistant",
            "content": reply
        })

        # save back
        conversation_memory[session_id] = history

        return jsonify({
            "type": "text",
            "reply": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
