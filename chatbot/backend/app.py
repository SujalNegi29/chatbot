from flask import Flask, request, jsonify
from translator import detect_language, to_english, from_english
from rasa_client import send_to_rasa

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json.get("message")

    # 1️⃣ Detect language
    user_lang = detect_language(user_text)

    # 2️⃣ Translate to English
    english_text = to_english(user_text, user_lang)

    # 3️⃣ Send to Rasa
    rasa_response = send_to_rasa(english_text)

    # 4️⃣ Get bot reply
    bot_english = rasa_response[0]["text"]

    # 5️⃣ Translate back
    bot_final = from_english(bot_english, user_lang)

    return jsonify({
        "reply": bot_final,
        "language": user_lang
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
