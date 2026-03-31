from flask import Flask,render_template,request,jsonify
import os
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods=["POST","GET"])
def takeinput():
        
    if request.method == "POST":
        
        try:
            user_input = request.json.get('user_input_field_name')
            completion = client.responses.create(
                model="gpt-4o-mini",
                input=user_input
            )
            return jsonify({"reply": completion.output_text})


        except Exception as e:
            return jsonify({"error":str(e)}),500



if __name__ == "__main__":
    app.run(debug=True)
