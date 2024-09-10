from line_bot_api import *
from urllib.parse import parse_qsl
import datetime
from extensions import db
from models.user import User
from models.reservation import Reservation

LINE_CHANNEL_ACCESS_TOKEN = 'ixxJyMhiYZvVR2K+lichfu1MH8pUm6kwo7/WjwOminJNM9O658GCQ/6742DqxaP5b9DUNrMSgDUij+q6lRCdfa70qRoYuh3vQ78Zywi5p/SBHowVNFxTNFu4zQH/cyuqVAQZVCFDa9m/UHU8amdo7AdB04t89/1O/w1cDnyilFU='
 
LINE_CHANNEL_SECRET = 'ad510521e72727441a21d56fb8453180'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


services = {
    1: {
        'itemid': '1',
        'img_url': 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"',
        'title': '測試標題一a',
        'duration': '內容一a',
        'post_url': 'https://linecorp.com'
    },
    2: {
        'itemid': '1',
        'img_url': 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"',
        'title': '測試標題一b',
        'duration': '內容一b',
        'post_url': 'https://linecorp.com'
    },
    3: {
        'itemid': '2',
        'img_url': 'https://st3.depositphotos.com/4676639/15203/i/600/depositphotos_152030606-free-stock-photo-kitten-and-adult-cat-breed.jpg',
        'title': '測試標題二a',
        'duration': '內容二a',
        'post_url': 'https://linecorp.com'
    },
    4: {
        'itemid': '2',
        'img_url': 'https://st3.depositphotos.com/4676639/15203/i/600/depositphotos_152030606-free-stock-photo-kitten-and-adult-cat-breed.jpg',
        'title': '測試標題二b',
        'duration': '內容二b',
        'post_url': 'https://linecorp.com'
    },
}

week=['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']




def service_category_event(event):
    print(event)


def service_event(event):
    flex_message = FlexSendMessage(
        alt_text='預約時間',
        contents={
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://plus.unsplash.com/premium_photo-1661603829936-a1416387b34d?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
            "type": "uri",
            "uri": "https://line.me/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "預約項目",
                "weight": "bold",
                "size": "xl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "說明",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": "根據需求選擇預約項目",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "所需時間",
                        "color": "#aaaaaa",
                        "size": "sm",
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": "30-120分鐘",
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
                    }
                    ]
                }
                ]
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "postback",
                "label": "頭皮檢測",
                "data": "action=book&itemid=examine",
                "displayText": "頭皮檢測"
                }
            },
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "postback",
                    "label": "頭皮護理",
                    "data": "action=book&itemid=scalpcare",
                    "displayText": "頭皮護理"
                    }
                }
                ],
                "flex": 0
            }
            ],
            "flex": 0
        }
        }


    )
    line_bot_api.reply_message(
        event.reply_token,
        [flex_message]
    )

def booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='已與你有約',
                text=f'{reservation.booking_service}\n預約時間: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='取消預約',
                        display_text='postback text',
                        data='action=canceled'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
        event.reply_token,
        [buttons_template_message])

        return True
    else:
        return False
    

def service_select_event(event):
    # data = dict(parse_qsl(event.postback.data))
    # quick_reply_buttons = []
    # today = datetime.datetime.today().date()

    # for x in range(1, 8):
    #     day = today + datetime.timedelta(days=x)
        
    #     quick_reply_button = QuickReplyButton(
    #             action=PostbackAction(label=f'{day}',
    #                                 text=f'{day}',
    #                                 data=f'action=select_time&date={data}')
    #         )
    #     quick_reply_buttons.append(quick_reply_button)
    #     print(quick_reply_button)
    # text_message = TextSendMessage(text='你想要哪天呢？',
    #                                quick_reply=QuickReply(items=quick_reply_buttons))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     [text_message]
    # )
    user = User.query.filter(User.line_id == event.source.user_id).first()
    if booked(event, user):
        return 
    data = dict(parse_qsl(event.postback.data))
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=30)  # 允許選擇未來30天內的日期

    datetime_picker = TemplateSendMessage(
        alt_text='選擇日期',
        template=ButtonsTemplate(
            title='選擇預約日期',
            text='請選擇您想要的日期',
            actions=[
                DatetimePickerAction(
                    label='選擇日期',
                    data=f'action=select_time&itemid={data["itemid"]}',
                    mode='date',
                    initial=today.isoformat(),
                    min=today.isoformat(),
                    max=max_date.isoformat()
                )
            ]
        )
    )
    # text_message = TextSendMessage(text='你想要哪天呢？',
    #                                quick_reply=QuickReply(items=datetime_picker))
    line_bot_api.reply_message(
        event.reply_token,
        [datetime_picker]
    )
def handle_date_selection(event):
    selected_date = event.postback.params['date']
    # 這裡你可以處理選擇的日期，例如保存到數據庫或進行下一步操作
    response_message = TextSendMessage(text=f'您選擇: {selected_date}\n接下來請選擇時間')
    
    # 這裡你可以添加選擇時間的邏輯，例如調用 service_select_time_event
    line_bot_api.reply_message(event.reply_token, [response_message])

def service_select_time_event(event):

    selected_date = str(event.postback.params['date'])
    # 這裡你可以處理選擇的日期，例如保存到數據庫或進行下一步操作
    weekday = selected_date.weekday()
    response_message = TextSendMessage(text=f'您選擇: {selected_date}{week[weekday]}\n接下來請選擇時間')
    
    # 這裡你可以添加選擇時間的邏輯，例如調用 service_select_time_event
    # line_bot_api.reply_message(event.reply_token, [response_message])

    
    data = dict(parse_qsl(event.postback.data))
    quick_reply_buttons = []
    book_time = ['09:00', '11:00', '13:00', '15:00', '17:00']
    for time in book_time:
        quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=time,
                                    text=f'{time}',
                                    data=f'action=confirm&time={time}&date={selected_date}&itemid={data["itemid"]}'))
        quick_reply_buttons.append(quick_reply_button)
    text_message = TextSendMessage(text='你想要哪個時段？',
                                    quick_reply=QuickReply(items=quick_reply_buttons))
    line_bot_api.reply_message(
        event.reply_token,
        [response_message,text_message]
    )

def confirm_event(event):
    data = dict(parse_qsl(event.postback.data))
    confirm_template_message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text=f'請確認時段\n\n日期: {data["date"]} \n時段: {data["time"]}\n\n資料是否正確?',
            actions=[
                PostbackAction(
                    label='是',
                    display_text='資料正確，我將準時前往！',
                    data=f'action=confirmed&time={data["time"]}&date={data["date"]}&itemid={data["itemid"]}'
                ),
                MessageAction(
                    label='否',
                    text='資料有誤，想重新選擇。'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message]
    )

def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = data['itemid']
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    print(booking_datetime)

    user =User.query.filter(User.line_id == event.source.user_id).first()

    reservation = Reservation(
        user_id=user.id,
        booking_service_itemid=booking_service,
        booking_service=booking_service,
        booking_datetime=booking_datetime
    )

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='感謝你的預約！')]
    )




    
def service_canceled_event(event):
    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='已取消預約')]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='尚未預約')]
        )