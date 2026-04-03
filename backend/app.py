from flask import Flask,render_template,request,jsonify
import os
from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI( base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-OpenRouter-Title": "Concept Mapper"
    }
    )
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
            "content": str(user_input)}        )


        # call AI with FULL history
        completion = client.chat.completions.create(

            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are an expert learning path generator.

                        Your behavior has TWO phases:

                        ---------------------
                        PHASE 1: DISCOVERY
                        ---------------------
                        - Ask exactly 2-3 clarification questions.
                        - Keep them short and clear.
                        - DO NOT generate JSON in this phase.

                        ---------------------
                        PHASE 2: GRAPH GENERATION
                        ---------------------
                        - After enough context, generate a learning path as JSON.
                        - Output ONLY valid JSON.
                        - DO NOT include explanations.
                        - DO NOT use markdown (no ```).
                        - Output must start with { and end with }.

                        ---------------------
                        STRICT JSON FORMAT
                        ---------------------
                        {
                        "type":"graph"
                        "nodes": [
                            {
                            "id": "string",
                            "label": "short name",
                            "description": "2-3 lines",
                            "type": "foundation/core/advanced/project",
                            "x": number,
                            "y": number,
                            "z": number
                            }
                        ],
                        "edges": [
                            {
                            "from": "node_id",
                            "to": "node_id"
                            }
                        ]
                        }

                        ---------------------
                        EXAMPLE (FEW-SHOT)
                        ---------------------

                        User: I want to learn Python for AI

                        Assistant:
                        {
                        "type":"graph"
                        "nodes": [
                            {
                            "id": "1",
                            "label": "Python Basics",
                            "description": "Variables, loops, functions and syntax fundamentals.",
                            "type": "foundation",
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                            {
                            "id": "2",
                            "label": "Data Structures",
                            "description": "Lists, dictionaries, sets and their usage.",
                            "type": "core",
                            "x": 2,
                            "y": 1,
                            "z": 0
                            },
                            {
                            "id": "3",
                            "label": "NumPy & Pandas",
                            "description": "Data handling and numerical computation.",
                            "type": "core",
                            "x": 4,
                            "y": 2,
                            "z": 0
                            }
                        ],
                        "edges": [
                            { "from": "1", "to": "2" },
                            { "from": "2", "to": "3" }
                        ]
                        }

                        ---------------------
                        FINAL RULES
                        ---------------------
                        - NEVER mix text with JSON.
                        - NEVER explain JSON.
                        - NEVER output invalid JSON.
                        - ALWAYS follow the structure exactly.
                        """
                },
                *history   # 👈 THIS IS THE MAGIC FIX
            ]
        )

        print(completion)
        reply = completion.choices[0].message.content
        print(reply)
        # add AI reply to history

        history.append({
            "role": "assistant", 
            "content": str(reply)
            })
        
        print("REPLY RAW:", reply)
        # save back
        conversation_memory[session_id] = history
        try:
            graph_data = json.loads(reply)
            return jsonify({
        "type": "graph",
        "graph": graph_data
        })
        except:

            return jsonify({
                "type": "text",
                "reply": reply
            })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
