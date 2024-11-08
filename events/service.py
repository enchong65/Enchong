from line_bot_api import *
from urllib.parse import parse_qsl
import datetime
from datetime import timedelta
from extensions import db
from models.user import User
from models.reservation import Reservation, TimeSlot

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

book_list ={
    '一':['10:30', '11:00', '13:30', '14:00', '15:30', '16:00', '18:00', '18:30', '19:00'],
    '二':['10:30', '11:00', '13:30', '14:00', '15:30', '16:00', '18:00', '18:30', '19:00'],
    '三':['10:30', '11:00', '13:30', '14:00', '15:30', '16:00', '18:00', '18:30', '19:00'],
    '四':['10:30', '11:00', '13:30', '14:00', '15:30', '16:00', '18:00', '18:30', '19:00'],
    '五':['10:30', '11:00', '13:30', '14:00', '15:30', '16:00', '18:00', '18:30', '19:00'],
    '六':['10:30', '11:00', '12:00', '12:30', 
                 '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00'],
    '日':['13:30', '14:30'],
}


def service_category_event(event):
    print(event)


def service_event(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_datetime > datetime.datetime.now()).first()
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
                "label": "取消預約" if reservation and reservation.booking_service=='頭皮檢測' else '頭皮檢測',
                "data": "action=book&itemid=examine",
                "displayText": "取消預約" if reservation and reservation.booking_service=='頭皮檢測' else '頭皮檢測'
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
                    "label": "取消預約" if reservation and reservation.booking_service=='頭皮護理' else '頭皮護理',
                    "data": "action=book&itemid=scalpcare",
                    "displayText": "取消預約" if reservation and reservation.booking_service=='頭皮護理' else '頭皮護理'
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
                title='已與你有約，確定要取消嗎？',
                text=f'{reservation.booking_service}\n預約時間: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='確定取消',
                        display_text='抱歉，我確定取消預約',
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
    

def is_time_slot_available(date, time):
    selected_date = date
    formate_date = selected_date.split('-')
    weekday = datetime.date(int(formate_date[0]),int(formate_date[1]),int(formate_date[2])).weekday()
    week = ['一', '二', '三', '四', '五', '六', '日']
    start_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(hours=2)
    
    affected_slots = TimeSlot.query.filter(
        TimeSlot.date == start_datetime.date(),
        TimeSlot.time >= start_datetime.time(),
        TimeSlot.time < end_datetime.time()
    ).all()
    if week[weekday] == '六':
        return all(slot.count < 2 for slot in affected_slots) and sum(slot.count for slot in affected_slots) < 32 #test
    elif week[weekday] == '日':
        return all(slot.count < 1 for slot in affected_slots)
    else:
        if time in ['10:30', '11:00']:
            return all(slot.count < 1 for slot in affected_slots)
        else:
            return all(slot.count < 2 for slot in affected_slots)


def get_available_time_slots(date):
    selected_date = date
    formate_date = selected_date.split('-')
    weekday = datetime.date(int(formate_date[0]),int(formate_date[1]),int(formate_date[2])).weekday()
    week = ['一', '二', '三', '四', '五', '六', '日']
    all_slots = book_list[week[weekday]]
    available_slots = []

    for time in all_slots:
        # 先檢查資料庫中是否存在該日期和時間段的 TimeSlot
        start_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        
        # 查找資料庫中是否已存在該時間段的記錄
        slot = TimeSlot.query.filter_by(date=start_datetime.date(), time=start_datetime.time()).first()

        if not slot:
            # 如果資料庫中不存在該記錄，則創建一個新的
            slot = TimeSlot(date=start_datetime.date(), time=start_datetime.time())
            db.session.add(slot)
            db.session.commit()  # 保存新的 TimeSlot 到資料庫

        # 檢查該時間段是否可用
        if is_time_slot_available(date, time):
            available_slots.append(time)

    return available_slots

def update_time_slots(date, time):
    start_datetime = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(hours=2)

    affected_slots = TimeSlot.query.filter(
        TimeSlot.date == start_datetime.date(),
        TimeSlot.time >= start_datetime.time(),
        TimeSlot.time < end_datetime.time()
    ).all()

    for slot in affected_slots:
            slot.count += 1


    db.session.commit()

def service_select_event(event):
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
    response_message = TextSendMessage(text=f'您選擇: {selected_date}\n接下來請選擇時間，如沒有適合時段可直接點選上方「選擇日期」重新選擇')
    
    # 這裡你可以添加選擇時間的邏輯，例如調用 service_select_time_event
    line_bot_api.reply_message(event.reply_token, [response_message])

def service_select_time_event(event):
    selected_date = str(event.postback.params['date'])
    formate_date = selected_date.split('-')
    weekday = datetime.date(int(formate_date[0]),int(formate_date[1]),int(formate_date[2])).weekday()
    week = ['一', '二', '三', '四', '五', '六', '日']
    
    response_message = TextSendMessage(text=f'您選擇: {selected_date} 星期{week[weekday]}\n接下來請選擇時間\n\n如沒有適合時段可直接點選上方「選擇日期」重新選擇')
    
    data = dict(parse_qsl(event.postback.data))
    quick_reply_buttons = []
    available_times = get_available_time_slots(selected_date)
    
    for time in available_times:
        quick_reply_button = QuickReplyButton(
            action=PostbackAction(
                label=time,
                display_text=f'我要預約 {time}',
                data=f'action=confirm&time={time}&date={selected_date}&itemid={data["itemid"]}'
            )
        )
        quick_reply_buttons.append(quick_reply_button)
    
    if quick_reply_buttons:
        text_message = TextSendMessage(
            text='請選擇可用的時段：',
            quick_reply=QuickReply(items=quick_reply_buttons)
        )
        line_bot_api.reply_message(event.reply_token, [response_message, text_message])
    else:
        no_slot_message = TextSendMessage(text='很抱歉，該日期沒有可用的時段。請選擇其他日期。')
        line_bot_api.reply_message(event.reply_token, [response_message, no_slot_message])


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

    booking_service = '頭皮護理' if data['itemid'] == 'examine' else '頭皮檢測'
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    print(booking_datetime)

    date = data['date']
    time = data['time']
    
    if is_time_slot_available(date, time):
        update_time_slots(date, time)
        user =User.query.filter(User.line_id == event.source.user_id).first()

        reservation = Reservation(
            user_id=user.id,
            name = user.display_name,
            confirmed = False,
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
    else:
        error_message = TextSendMessage(text='很抱歉，該時段已被預約。請選擇其他時段。')
        line_bot_api.reply_message(event.reply_token, error_message)




    
def service_canceled_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                          Reservation.is_canceled.is_(False),
                                          Reservation.booking_datetime > datetime.datetime.now()).first()

    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        start_datetime = reservation.booking_datetime
        print(start_datetime)
        end_datetime = start_datetime + timedelta(hours=2)

        affected_slots = TimeSlot.query.filter(
            TimeSlot.date == start_datetime.date(),
            TimeSlot.time >= start_datetime.time(),
            TimeSlot.time < end_datetime.time()
        ).all()

        for slot in affected_slots:
                slot.count -= 1
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