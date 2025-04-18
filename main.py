from flask import Flask, request, jsonify
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# Lấy token từ biến môi trường
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Khởi tạo client OpenAI theo chuẩn mới
client = OpenAI(api_key=OPENAI_API_KEY)

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

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    print("Received data:", data)

    # Xác minh URL từ Slack (lần đầu)
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # Xử lý khi bot được mention
    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            user_message = event.get("text")
            channel_id = event.get("channel")
            print("User said:", user_message)

            # Gọi GPT
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Bạn là một trợ lý AI thân thiện."},
                        {"role": "user", "content": user_message}
                    ]
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"Lỗi khi gọi GPT: {str(e)}"
                print("OpenAI Error:", e)

            # Gửi trả lời về Slack
            send_message_to_slack(channel_id, answer)

    return "", 200

if __name__ == "__main__":
    app.run()