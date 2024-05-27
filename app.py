from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='aR1DU66u+SKzAsfyp7dEnXeXJRH8P4VhsqI6UIpuiTYmIPY8qGOl2peSyeiM0l7blFo74XvJ83h12yYuKFZzQo6FE7s6d+7uG4LzK72s/KmETtcF+yQKG2O9x6mSYLAIshpgTIopq5sJeqtGuZ834wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3d30dafe72d5f0975512a2a2ea8d77aa')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，您說什麼'

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = "還沒"
    elif msg == '你是誰'
        r == '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=r)]
            )
        )

if __name__ == "__main__":
    app.run()