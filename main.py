from flask import Flask, request, jsonify
import requests
import openai
app = Flask(__name__)
# Thay bằng token thật của bạn
# Set API key OpenAI từ biến môi trường
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
@app.route("/")
def home():
    return "Bot is running!"
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    print("Received data:", data)
    # Xác minh URL từ Slack lần đầu
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý thân thiện."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
            # Gửi lại trả lời vào Slack
            send_message_to_slack(channel_id, answer)
    return "", 200
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"
if __name__ == "__main__":
    app.run()
