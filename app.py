from flask import Flask, render_template, request, jsonify
from chatbot import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_input = request.form.get("msg")
        print("User input:", user_input)  # Debugging

        if not user_input:
            return jsonify({"response": "No message received."})

        bot_response = get_response(user_input)
        print("Bot response:", bot_response)  # Debugging

        return jsonify({"response": bot_response})

    except Exception as e:
        print("ERROR OCCURRED:", str(e))  # 🔥 See the actual error
        return jsonify({"response": "Oops! Something went wrong."})


if __name__ == "__main__":
    app.run(debug=True)
