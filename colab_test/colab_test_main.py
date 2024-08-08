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
LINE_CHANNEL_SECRET = "---"
LINE_CHANNEL_ACCESS_TOKEN = "---"
GEMINI_KEY  = "---"
########

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN) # 輸入 你的 Channel access token
        handler = WebhookHandler(LINE_CHANNEL_SECRET)        # 輸入 你的 Channel secret
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
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-pro')
            print(msg[6:])
            response = model.generate_content(msg[6:])
            reply_msg = response.text
            print(reply_msg)
        else:
            reply_msg = msg
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except:
        print('### error')   # 如果發生錯誤，印出收到的內容
        print(body)
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  app.run()