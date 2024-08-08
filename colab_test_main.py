#### success on Colab

from flask import Flask, request
from pyngrok import ngrok

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json

import google.generativeai as genai
import os

app = Flask(__name__)
port = "5000"

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\" ")

########
LINE_CHANNEL_SECRET = "0e93a12b4ee2537370fef5d562821961"
LINE_CHANNEL_ACCESS_TOKEN = "Xm8yQXdVj3MR/OnzmWPxMQkqZQdmUps5oD2DauG0CZnvprK/X+QVGSk2/Y/eEdlde67puqVbBT9fYYEC9UT7VtlLglUHp1oHVXPC4siiDRnBYEmshORy6yB/PluZjEJzbltAssIALrgmy0tH/bDt6QdB04t89/1O/w1cDnyilFU="
GEMINI_KEY  = "AIzaSyCQuq44s-xCiv5rEvPXiWYW_SDjSwYfuKU"
########

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)  # 輸入 你的 Channel access token
        handler = WebhookHandler(LINE_CHANNEL_SECRET)         # 輸入 你的 Channel secret
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        # 取出文字的前五個字元，轉換成小寫
        ai_msg = msg[:6].lower()
        reply_msg = ''
        print('error 0')
        # 取出文字的前五個字元是 hi ai:
        if ai_msg == 'hi ai:':
            print('error 1-0')
            genai.configure(api_key=GEMINI_KEY)
            print('error 1-1')
            model = genai.GenerativeModel('gemini-pro')
            print('error 1-2')
            print(msg[6:])
            response = model.generate_content("Write a story about an AI and magic")
            print('error 1-3')
            reply_msg = response.text
            print('error 1-4')
            print(reply_msg)
        else:
            reply_msg = msg
            print('error 2')
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)

        print('error 3')
    except:
        print('### error')   # 如果發生錯誤，印出收到的內容
        print(body)
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  app.run()