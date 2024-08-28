from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import FlexSendMessage
from events.basic import about_us_event
from events.service import *
from urllib.parse import parse_qsl
import os

LINE_CHANNEL_ACCESS_TOKEN = 'ixxJyMhiYZvVR2K+lichfu1MH8pUm6kwo7/WjwOminJNM9O658GCQ/6742DqxaP5b9DUNrMSgDUij+q6lRCdfa70qRoYuh3vQ78Zywi5p/SBHowVNFxTNFu4zQH/cyuqVAQZVCFDa9m/UHU8amdo7AdB04t89/1O/w1cDnyilFU='
 
LINE_CHANNEL_SECRET = 'ad510521e72727441a21d56fb8453180'
line_bot_api = LineBotApi(os.environ.get('CHAANNEL_ACCESS_TOKEN',LINE_CHANNEL_ACCESS_TOKEN))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET',LINE_CHANNEL_SECRET))