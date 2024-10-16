from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from pytz import timezone
from models.user import User
from models.reservation import Reservation
from extensions import db
from line_bot_api import line_bot_api
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageAction

scheduler = APScheduler()

def send_reminder():
    with scheduler.app.app_context():
        now = datetime.now(timezone('UTC'))
        two_days_later = now + timedelta(days=2)
        reservations = Reservation.query.filter(
            Reservation.booking_datetime.between(two_days_later, two_days_later + timedelta(days=1)),
            Reservation.reminder_sent == False
        ).all()

        for reservation in reservations:
            user = User.query.get(reservation.user_id)
            user_tz = timezone(('UTC'))
            reservation_time_user_tz = reservation.booking_datetime.astimezone(user_tz)

            confirm_template = ConfirmTemplate(
                text=f'您有一個預約！\n \n預約時間：{reservation_time_user_tz.strftime("%Y-%m-%d %H:%M")}\n服務項目：{reservation.booking_service}\n請問您是否確定赴約？\n(已為您預留時間，請盡量赴約！謝謝)',
                actions=[
                    MessageAction(label='確定', text=f'確定赴約'),
                    MessageAction(label='取消', text=f'取消預約')
                ]
            )

            try:
                line_bot_api.push_message(
                    user.line_id,
                    TemplateSendMessage(alt_text='預約提醒', template=confirm_template)
                )
                reservation.reminder_sent = True
                db.session.commit()
            except Exception as e:
                print(f"Error sending reminder to user {user.line_id}: {str(e)}")

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='send_reminder', func=send_reminder, trigger='cron', hour=17, minute=22)