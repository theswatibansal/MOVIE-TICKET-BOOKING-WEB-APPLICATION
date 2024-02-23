from flask import Flask, render_template, request, redirect, url_for, session, flash
from newmodels import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy import func
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

# =================================== Configuration ===============================

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
app.secret_key = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

db.init_app(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================================== Controllers ==================================

@app.route("/", methods=["GET", "POST"])
@login_required
def venue():
    venues = Venue.query.all()
    return render_template("home.html", venues=venues)


@app.route('/venue')
def index():
    data = Venue.query.all()
    return render_template('index.html', venues=data)


@app.route('/user_venue')
@login_required
def user_venue():
    data = Venue.query.all()
    return render_template('user_venue.html', venues=data)


@app.route('/user_shows')
@login_required
def user_shows():
    data = Show.query.all()
    return render_template("user_show.html", shows=data)


@app.route('/see_user_show/<int:id>', methods=['GET', 'POST'])
def user_venue_show(id):
    v = Venue.query.get(id)
    shows = v.movie
    return render_template('user_ven_show.html', v=v, shows=shows)

@app.route('/auth')
def auth():
    return render_template('auth.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form['is_admin']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exit')
            return redirect(url_for('signup'))
        user = User(name=name, username=username, password=generate_password_hash(password,method='sha256'), is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id

            login_user(user)
        if not user or not check_password_hash(user.password, password):
            flash('Wrong credentials entered.')
            return redirect(url_for('login'))
        return render_template('home.html', user=current_user, username=username)
    return render_template('login.html')

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == "GET":
        return render_template("admin_signup.html")
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form['is_admin']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exit.')
            return redirect(url_for('admin_signup'))
        user = User(name=name, username=username, password=generate_password_hash(password,method='sha256'), is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return redirect("/admin_login")
    return render_template('admin_signup.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):

            login_user(user)
        if not user or not check_password_hash(user.password, password):
            flash('Wrong credentials entered.')
            return redirect(url_for('admin_login'))
        return redirect(url_for('index'))
    return render_template('admin_login.html')

@app.route("/venue/create", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        return render_template("all_venue_form.html")

    if request.method == 'POST':
        id = request.form.get("id")
        v_name = request.form.get("v_name")
        country = request.form.get("country")
        state = request.form.get("state")
        zip = request.form.get("zip")
        s_no = request.form.get("s_no")
        capacity = request.form.get("capacity")

        v = Venue(v_id=id, name=v_name, country=country, state=state, zip=zip, street_no=s_no, capacity=capacity,
                  movie=[])

        db.session.add(v)
        db.session.commit()

        return redirect('/venue')


@app.route("/venue/<int:v_id>/delete")
def del_venue(v_id):
    data = Venue.query.filter(Venue.v_id == v_id).one()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route("/venue/<int:v_id>/update", methods=["GET", "POST"])
def update_venue(v_id):
    if request.method == "GET":
        data = Venue.query.filter(Venue.v_id == v_id).first()
        sho = Show.query.all()
        return render_template("update_venue.html", venues=data, shows=sho)

    else:
        uv = Venue.query.filter_by(v_id=v_id).first()

        uv.v_name = request.form.get("v_name")
        uv.country = request.form.get("country")
        uv.state = request.form.get("state")
        uv.zip = request.form.get("zip")
        uv.s_no = request.form.get("s_no")
        uv.capacity = request.form.get("capacity")
        db.session.add(uv)

        db.session.commit()
        return redirect('/venue')


@app.route('/shows')
def all_shows():
    data = Show.query.all()
    return render_template("index_show.html", shows=data)


@app.route("/show/create", methods=["GET", "POST"])
def add_show():
    if request.method == "GET":
        return render_template("all_show_form.html")

    if request.method == 'POST':
        id = request.form.get("id")
        s_name = request.form.get("s_name")
        s_timing = request.form.get("s_timing")
        e_timing = request.form.get("e_timing")
        rating = request.form.get("rating")
        tag = request.form.get("tag")
        date = request.form.get("date")
        language = request.form.get("language")
        format = request.form.get("format")
        price = request.form.get("price")
        seats_booked = request.form.get("seats_booked")

        s = Show(s_id=id, name=s_name, start_timing=s_timing, end_timing=e_timing, rating=rating, tag=tag,
                 release_date=date, language=language, format=format, price=price, seats_booked=seats_booked)

        db.session.add(s)
        db.session.commit()

        return redirect('/shows')


@app.route("/show/<int:s_id>/update", methods=["GET", "POST"])
def update_show(s_id):
    if request.method == "GET":
        data = Show.query.filter_by(s_id=s_id).first()
        # ven = Venue.query.all()
        return render_template("update_show.html", shows=data)

    else:
        us = Show.query.filter_by(s_id=s_id).first()

        us.s_name = request.form.get("s_name")
        us.s_timing = request.form.get("s_timing")
        us.e_timing = request.form.get("e_timing")
        us.rating = request.form.get("rating")
        us.tag = request.form.get("tag")
        us.date = request.form.get("date")
        us.language = request.form.get("language")
        us.format = request.form.get("format")
        us.price = request.form.get("price")
        us.seats_booked = request.form.get("seats_booked")
        db.session.add(us)
        db.session.commit()
        return redirect('/shows')


@app.route("/show/<int:s_id>/delete")
def del_show(s_id):
    data = Show.query.filter(Show.s_id == s_id).one()
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route('/see_show/<int:id>', methods=['GET', 'POST'])
def venue_show(id):
    v = Venue.query.get(id)
    shows = v.movie
    return render_template('ven_show.html', v=v, shows=shows)


@app.route('/assign/<int:id>', methods=['GET', 'POST'])
def assign(id):
    if request.method == 'GET':
        s = Show.query.get(id)
        venues = Venue.query.all()
        return render_template('assign_venue.html', venues=venues, s=s)
    if request.method == 'POST':
        s = Show.query.get(id)
        v_id = request.form.get('v_id')
        s.venue_id = v_id
        db.session.add(s)
        db.session.commit()
        return redirect('/')

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("login"))

@app.route("/admin_logout")
@login_required
def admin_log_out():
    logout_user()
    return redirect(url_for("admin_login"))


@app.route("/search", methods = ['GET', 'POST'])
@login_required
def search_entity():
    entry = request.form.get("entry")
    tag = Show.query.filter(Show.tag == entry).all()
    all_shows = Show.query.filter(Show.name == entry).all()
    all_venues = Venue.query.filter(Venue.name == entry).all()
    if all_shows != []:
        return render_template("result_show.html", shows=all_shows)
    if tag != []:
        return render_template("result_show.html", shows=tag)
    if all_venues != []:
        return render_template("result_venue.html", venues=all_venues)
    return render_template("search.html")

@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    if request.method == 'GET':
        s = Show.query.get(id)
        price = s.price
        seats_booked = s.seats_booked

        v_id = s.venue_id
        v = Venue.query.get(v_id)
        capacity = v.capacity
        available_seats = int(capacity)-int(seats_booked)


        return render_template('book_assign_venue.html', s=s, capacity=capacity, price=price, seats_booked=seats_booked, available_seats=available_seats)
    if request.method == 'POST':
        s = Show.query.get(id)
        #user_id = session.get('user_id')
        s_seats = request.form.get("s_seats")
        s_seats = int(s_seats)

        seats_booked = s.seats_booked
        seats_booked = int(seats_booked) + int(s_seats)
        v_id = s.venue_id
        v = Venue.query.get(v_id)
        capacity = v.capacity
        seats_booked = s.seats_booked

        available_seats = int(capacity) - int(seats_booked)

        if available_seats >= s_seats:
            user_id = session.get('user_id')
            b = Booking(show_id=id, seats_booked_by_user=s_seats, user_id=id)
            available_seats = request.form.get('available_seats')

            db.session.add(b)
            db.session.commit()
            flash("Your booking is successfully done.")
            return render_template("success.html")
        else:
            s = Show.query.get(id)
            name = s.name
            flash("Housefull for ")
            return render_template('house.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)


#in booking page
#take show id which is in query string
#In get
    # Get price from show table using show id
    # Get seat booked from show table using show id
    # Get capacity from show join  venue (venue_id)
    # if seatbooked + sets he want to book < capacity
        # insert in booking table
        #show table update seatsbooked  = seatbooked + sets he want to book
    #else
        #show housefull
#on submit
#Insert in booking - already done
#in show table increase add seated bookid using show id


