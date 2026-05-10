from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

api_url = "https://us-central1-ai-chat-bot-bf47e.cloudfunctions.net/chat_function_android"

headers = {
    'User-Agent': "okhttp/5.1.0",
    'Accept-Encoding': "gzip",
    'content-type': "application/json; charset=utf-8"
}

users_online = set()
total_visits = 0


@app.route("/")
def home():
    return open("index.html", encoding="utf-8").read()


@app.route("/chat", methods=["POST"])
def chat():
    global total_visits

    user_ip = request.remote_addr
    users_online.add(user_ip)
    total_visits += 1

    user_message = request.json["message"]

    payload = {
        "data": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_message}
                    ]
                }
            ],
            "model": "gpt-4o"
        }
    }

    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        data = response.json()

        answer = data['result']['choices'][0]['message']['content']
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"reply": str(e)})


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "online": len(users_online),
        "total": total_visits
    })


if __name__ == "__main__":
    app.run()
