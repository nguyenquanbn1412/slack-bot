from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

def send_message_to_slack(channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Slack response:", response.text)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    print("Received data:", data)

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            user_message = event.get("text")
            channel_id = event.get("channel")
            print("User said:", user_message)

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Bạn là một trợ lý thân thiện."},
                        {"role": "user", "content": user_message}
                    ]
                )
                answer = response["choices"][0]["message"]["content"]
                send_message_to_slack(channel_id, answer)
            except Exception as e:
                print("OpenAI Error:", e)
                send_message_to_slack(channel_id, "Xin lỗi, bot hiện đang gặp lỗi!")

    return "", 200

if __name__ == "__main__":
    app.run()
