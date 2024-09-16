from extensions import db
import datetime

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booking_service_itemid = db.Column(db.String(50), nullable=False)
    booking_service = db.Column(db.String(150), nullable=False)
    booking_datetime = db.Column(db.DateTime, nullable=False)

    is_canceled = db.Column(db.Boolean(), server_default='0')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())


    def __init__(self, user_id, booking_service_itemid, booking_service, booking_datetime):
        self.user_id = user_id
        self.booking_service_itemid = booking_service_itemid
        self.booking_service = booking_service
        self.booking_datetime = booking_datetime

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    count = db.Column(db.Integer, default=0)

    def __init__(self, date, time):
        self.date = date
        self.time = time

# class Booking(db.Model):
#     __tablename__ = 'bookings'
#     id = db.Column(db.Integer, primary_key=True)
#     line_user_id = db.Column(db.String(50), nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     service_id = db.Column(db.String(50), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)