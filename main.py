from flask import Flask, request, jsonify  # đảm bảo có import jsonify
import openai
import os
import requests
app = Flask(__name__)
# Set API key OpenAI từ biến môi trường
openai.api_key = os.environ.get("OPENAI_API_KEY")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
# Hàm gửi phản hồi về Slack
def send_message(channel, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }
    payload = {
        'channel': channel,
        'text': text
    }
    requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=payload)
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    # Xử lý xác minh ban đầu từ Slack
    if data.get("type") == "url_verification":
        return jsonify({'challenge': data["challenge"]})
    # Nếu là event thực tế (mention bot,...)
    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            user_message = event.get("text")
            channel_id = event.get("channel")
            # Gửi tới OpenAI và phản hồi...
            # [Phần xử lý chat ở đây giữ nguyên như cũ]
    return "", 200
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
if __name__ == "__main__":
    app.run()
