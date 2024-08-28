from line_bot_api import *

def about_us_event(event):
    emoji=[
                    {
                        'index': 2, 
                        'productId': '5ac1bfd5040ab15980c9b435', 
                        'emojiId': '009'
                    },
                ]  
    text_message = TextSendMessage(text='你好$\n你的堂數剩下：Ｏ堂',emojis=emoji)

