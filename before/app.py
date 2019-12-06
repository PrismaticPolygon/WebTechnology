from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm:

    def __init__(self):

        self.username = StringField("Username", validators=[DataRequired()])
        self.password = PasswordField("Password", validators=[DataRequired()])

        self.remember_me = BooleanField("Remember me")
        self.submit = SubmitField("Sign In")



login_manager = LoginManager()
app = Flask(__name__)

login_manager.init_app(app)

app.config["SECRET_KEY"] = "THIS IS A SECRET KEY"

app.secret_key = "THIS IS A SECRET KEY"

# So this is fairly simple.

@app.route('/')
def home():

    if current_user.is_authenticated:

        flash("You are logged in")

        return render_template("user.html")

    else:

        flash("You are not logged in")

        return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):

    # Given a user_id, load the appropriate User Object.
    # Does this even make sense?
    # Yes, actually. I can load ratings and what not.
    # Nice.
    # Then we can internalise it, and store it for later...

    # I really CBA to do this.

    # User class needs

    return {
        "user_id": 1,


    }


# I wonder whether I should do this properly. Internationlaisation and all that.
# Christ we've been indexing for a while.
# How big is this?

# So we login here.
#

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for("home"))

@app.route("/user")
@login_required
def user():

    pass

@app.route('/login', methods=['GET', "POST"])
def login():

    print(request.method)

    if request.method == 'POST':    # We're trying to login

        # And then here we call get_user.

        user = int(request.form['id'])

        # So here we're supposed to get the user schizzle. Unfortunately, all I can return is their recommendations.

        login_user(user, remember=True)

        flash("Logged in successfully")

        # next = request.args.get("next")

        # If url is not safe
        # if not is_safe_url(next):
        #
        #     return abort(400)

        session["username"] = user

        # ratings = get_user_ratings(user)
        # recommendations = get_user_recommendations(user)
        #
        # response = make_response(render_template("user.html", ratings=ratings, recommendations=recommendations))

        response = make_response(render_template("user.html"))

        return response

    else:   # We're just on the login page; return the appropriate template.

        return render_template('login.html')


if __name__ == "__main__":

    app.run()