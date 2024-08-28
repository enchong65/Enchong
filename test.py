from flask import Flask, request, abort
import sys
import logging

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

configuration = Configuration(access_token='ixxJyMhiYZvVR2K+lichfu1MH8pUm6kwo7/WjwOminJNM9O658GCQ/6742DqxaP5b9DUNrMSgDUij+q6lRCdfa70qRoYuh3vQ78Zywi5p/SBHowVNFxTNFu4zQH/cyuqVAQZVCFDa9m/UHU8amdo7AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ad510521e72727441a21d56fb8453180')

# logging.basicConfig(filename='app.log', level=logging.DEBUG)
# @app.route("/callback", methods=['POST'])
# def callback():
#     # # get X-Line-Signature header value
#     # signature = request.headers['X-Line-Signature']

#     # # get request body as text
#     # body = request.get_data(as_text=True)
#     app.logger.info("Received a request. Returning 200 OK.")    
#     print("Received webhook")
#     # print("Headers:", request.headers)
#     # print("Body:", request.get_data(as_text=True))
#     # # handle webhook body
#     # try:
#     #     handler.handle(body, signature)
#     # except InvalidSignatureError:
#     #     app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
#     #     abort(400)

#     return 'OK', 200


# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )
@app.route("/callback", methods=['POST'])
def callback():
    print("Received webhook")
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    print("Received webhook")
    print("Headers:", request.headers)
    print("Body:", body)
    sys.stdout.flush()
    # app.logger.info("Received a request to /callback")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK', 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )
@app.route("/test", methods=['GET'])
def test():
    app.logger.debug("Test route called")
    return "Hello, LINE Bot!", 200

if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")