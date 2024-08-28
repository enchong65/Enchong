from line_bot_api import *

from models.reservation import Reservation
import datetime

def list_reservation_event(event):
    reservations = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            Reservation.booking_datetime > datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()
    reservation_data_text = '今日行程\n\n'
    for reservation in reservations:
        reservation_data_text = reservation_data_text + f'''時間: {reservation.booking_datetime}\n項目: {reservation.booking_service}\n姓名: {reservation.user.display_name}\n'''
    print(reservations)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reservation_data_text)
    )        