import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

########
LINE_CHANNEL_SECRET = "---"
LINE_CHANNEL_ACCESS_TOKEN = "---"
########

def linebot(request):
    try:
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(LINE_CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        msg = json_data['events'][0]['message']['text']
        tk = json_data['events'][0]['replyToken']
        line_bot_api.reply_message(tk,TextSendMessage(msg))
        print(msg, tk)
    except:
        print(request.args)
    return 'OK'