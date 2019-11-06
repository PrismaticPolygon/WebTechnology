from flask import Flask, render_template, request, make_response
from main import get_user_recommendations, get_user_ratings

app = Flask(__name__)

@app.route('/')
def hello_world():

    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        user = int(request.form['id'])

    ratings = get_user_ratings(user)
    recommendations = get_user_recommendations(user)

    response = make_response(render_template("user.html", ratings=ratings, recommendations=recommendations))

    return response


if __name__ == "__main__":

    app.run()