from flask import Flask, redirect, url_for, flash, session, request, render_template
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, text, cast, Date
import requests
import config

# app = Flask(__name__)
# app.secret_key = "hi"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # users in the name of the table
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.permanent_session_lifetime = timedelta(days=5)
# 
# db = SQLAlchemy(app)



class business(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    term = db.Column(db.String(100))
    location = db.Column(db.String(100))


    def __init__(self, term, location):
        self.term   = term
        self.location = location



@app.route('/')
def homepage():
    return render_template("home.html", content="Testing")


@app.route('/home.html')
def home():
    return render_template("home.html", content="Testing")


@app.route("/view.html", methods=["POST", "GET"])
def view():
    # if request.method == "POST":
    #     session.permanent = True
    #     term = request.form['term']
    #     location = request.form["location"]
    #
    #     found_user = business.query.filter_by(name=term).first()
    #     if found_user:
    #         session["term"] = found_user.term
    #         session["location"] = found_user.term
    #
    #     else:
    #         usr = business(term, location)
    #
    #         db.session.add(usr)
    #         db.session.commit()
    #
    #     return redirect(url_for("ab2"))
    #
    # else:
    #     return render_template("view.html")
    if request.method == "POST":
        url = "https://api.yelp.com/v3/businesses/search"
        api_key = "ue-myw5IXut9n9rC6vYkfZBMCr3nw12DQh7iWQdjbAiQqpsldRKEenYM_1tMWih5YXeRu8CZVeuE6eNfq_9ItGpC-xwcm5np549SIjI7XWcm1jVxHb80n_I-oqTOX3Yx"

        headers = {"Authorization": "Bearer " + config.api_key}
        params = {
            # "term": "Food",
            # "location": "Jyväskylä"
            # "term": "Barber",
            # "location": "NYC"
            # "term": "Bar",
            # "location": "Jyväskylä"
            #  "term": "food",
            # "location": "Jyväskylä"
            # "term": "gym",
            # "location": "Helsinki"
            "term": request.form["term"],
            "location": request.form["location"]}
        response = requests.get(url, headers=headers, params=params)
        # print(response.text)
        businesses = response.json()["businesses"]
        # print(businesses)
        # List comprehension [item for item in list]
        names = [business["name"] for business in businesses if business["rating"] > 4.5]
        #print(names)
        return redirect(url_for("businesslist"))
    else:
        return render_template("view.html")


@app.route('/abb.html')
def businessList():
    #return f"<h1>Hello {name}, you are welcome</h1>"
    return render_template("businessList.html")


if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)

