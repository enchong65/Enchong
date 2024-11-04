from flask import Flask, request, abort
from extensions import db, migrate
from models.user import User
from line_bot_api import *
from events.admin import *
from events.scheduler import init_scheduler
from sqlalchemy import desc
#======python的函數庫==========

app = Flask(__name__)
# app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.ProdConfig'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Timmy055055@localhost:5432/Enchong'
db.app = app
db.init_app(app)
migrate.init_app(app, db)
init_scheduler(app)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=str(event.message.text)
    user = User.query.filter(User.line_id == event.source.user_id).first()
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)
        # print(profile.display_name)
        # print(profile.user_id)
        # print(profile.picture_url)
        # print(profile.status_message)
        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()
    
    if msg =='堂數顯示':
        about_us_event(event)
    if msg =='我要預約':
        # service_category_event(event)
        service_event(event,user)
    elif msg.startswith('*'):
        if event.source.user_id not in ['U5bbd73b1091f77b5de8e32e21b7bbc47','Uadad19504e6ebdccb706bd5d26031d37']:
            return
        if msg in ['*data', '*d']:
            list_reservation_event(event)
        if msg.startswith("*手動"):
            manipulation(event)
    else:
        text_message = TextSendMessage(msg)
    # line_bot_api.reply_message(event.reply_token, text_message)
    
    
    
    if msg.startswith('確定赴約'):
        reservations = Reservation.query.filter_by(user_id=user.id).order_by(desc(Reservation.booking_datetime)).all()
        # reservation = Reservation.query.get(reservation_id)
        if reservations:
            reservation = reservations[0]
            reservation.confirmed = True
            db.session.commit()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='感謝您的確認，我們期待您的到來！')
            )
    elif msg.startswith('取消預約'):
        reservations = Reservation.query.filter_by(user_id=user.id).order_by(desc(Reservation.booking_datetime)).all()
        # reservation = Reservation.query.get(reservation_id)
        if reservations:
            reservation = reservations[0]
            db.session.delete(reservation)
            db.session.commit()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您的預約已取消。\n如需重新預約，請於選單點選預約時間。')
            )
# @handler.add(PostbackEvent)
# def handle_message(event):
    # print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data.get('action') == 'book':
        # service_event(event)
        service_select_event(event)
    elif data.get('action') == 'select_date':
        handle_date_selection(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'canceled':
        service_canceled_event(event)
    print('date:', data.get('date'))
    print('time:', data.get('time'))
    print('action:', data.get('action'))
    print('itemid:', data.get('itemid'))
    print('service:', data.get('service_id'))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)