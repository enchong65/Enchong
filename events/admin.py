from line_bot_api import *
from models.user import User
from models.reservation import Reservation
import datetime

def list_reservation_event(event):
    reservations = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            # Reservation.confirmed.is_(True),
                                            Reservation.booking_datetime > datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()
    reservation_data_text = '所有行程\n\n'
    for reservation in reservations:
        confirmed = "" if reservation.confirmed else "(待確認)"
        reservation_data_text = reservation_data_text + f'''時間: {reservation.booking_datetime}\n項目: {reservation.booking_service}\n姓名: {reservation.user.display_name} {confirmed}\n\n'''
    print(reservations)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reservation_data_text)
    )        


def manipulation(event):
    data = event.message.text.split("\n")
    name = data[1]
    time = data[2]
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    service = data[3]

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation(
            user_id=user.id,
            name = name,
            booking_service_itemid=service,
            booking_service=service,
            booking_datetime=time,
            confirmed = True
            )

    db.session.add(reservation)
    db.session.commit()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"已加入新行程：\n姓名：{name}\n時間：{time}\n項目：{service}")
    )        