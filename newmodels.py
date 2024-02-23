from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

#one to many relation between venue and show, user and booking, show and booking
class Venue(db.Model):
    v_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    street_no = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    movie = db.relationship('Show', backref="theater")

    def __repr__(self):
        return f"<venue {self.name}>"


class Show(db.Model):
    s_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(20), nullable=False)
    start_timing = db.Column(db.String(20), nullable=False)
    end_timing = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.String(20), nullable=False)
    tag = db.Column(db.String(20), nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    format = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seats_booked = db.Column(db.Integer)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.v_id"))
    theaternew= db.relationship('Venue', back_populates="movie")
    booknew = db.relationship('Booking')


    #asso = db.relationship('association', backref="movie")
    def __repr__(self):
        return f"<show {self.name}>"

#class association(db.Model):
   # venue_id = db.Column(db.Integer, db.ForeignKey("venue.v_id"), primary_key = True)
   # show_id = db.Column(db.Integer, db.ForeignKey("show.s_id"), primary_key = True, unique=True)
   # maker = db.Column(db.Integer, db.ForeignKey("show.s_id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.String(20))
    book = db.relationship('Booking')


class Booking(db.Model):
    booking_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    show_id = db.Column(db.Integer, db.ForeignKey("show.s_id"))
    seats_booked_by_user = db.Column(db.Integer, nullable=False)
    #movie = db.relationship('Show')
