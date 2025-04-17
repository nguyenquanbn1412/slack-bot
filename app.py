from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import openai
import os
# Load biến môi trường
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Cấu hình Slack bot
app = App(token=SLACK_BOT_TOKEN)
# Cấu hình OpenAI
openai.api_key = OPENAI_API_KEY
# Lắng nghe tất cả tin nhắn có chứa tên bot hoặc trong tin nhắn trực tiếp
@app.event("app_mention")
@app.event("message")
def handle_message_events(body, message, say):
    user_text = message.get("text", "")
    # Gọi OpenAI API để lấy phản hồi
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # hoặc "gpt-3.5-turbo" nếu bạn muốn tiết kiệm
            messages=[{"role": "user", "content": user_text}]
        )
        ai_reply = response.choices[0].message['content']
        say(ai_reply)
    except Exception as e:
        say(f"Bot gặp lỗi: {e}")
# Chạy bot với SocketModeHandler
if __name__ == "__main__":
    print("Bot đang chạy...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
