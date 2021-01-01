import flask
from flask import Flask, request, render_template
import requests, config

app = Flask(__name__)
app.secret_key = "hi"


class business():

    def __init__(self, term, location):
        self.term = term
        self.location = location


@app.route('/')
def homepage():
    return render_template("home.html", content="Testing")


@app.route('/home.html')
def home():
    return render_template("home.html", content="Testing")


# Gets a list of the business names based on the search filters
@app.route("/view.html", methods=["POST", "GET"])
def jsonify():
    if request.method == "POST":
        url = "https://api.yelp.com/v3/businesses/search"

        headers = {"Authorization": "Bearer " + config.api_key}
        params = {

            "term": request.form["term"],
            "location": request.form["location"],
            "rating": request.form["rating"],
            "review_count": (request.form["review_count"])}
        response = requests.get(url, headers=headers, params=params)
        businesses = tuple(response.json()["businesses"])
        names = tuple([business["name"] for business in businesses if business["rating"]
                       > float(request.form["rating"]) and business["review_count"] >
                       int(request.form["review_count"])])
        rate = tuple([business["rating"] for business in businesses if business["name"] in names])
        review_count = tuple([business["review_count"] for business in businesses if business["name"] in names])
        display_phone = tuple([business["display_phone"] for business in businesses if business["name"] in names])
        is_closed = tuple([business["is_closed"] for business in businesses if business["name"] in names])
        location = tuple([business["location"] for business in businesses if business["name"] in names])
        # address1 = tuple([business["address1"] for business in businesses if business["name"] in names])
        business_location = request.form["location"]
        rating = request.form["rating"]
        term = request.form["term"]

        return flask.jsonify([{business_location: term}], [{'Name': names, 'Rating': rate, "Review Count": review_count,
                                                            'Display phone': display_phone, "is closed": is_closed,
                                                            "location": location}
                                                           for
                                                           names, rate, review_count, display_phone, is_closed, location
                                                           in
                                                           zip(names[::], rate[::], review_count[::], display_phone[::],
                                                               is_closed[::], location[::])])

       #Returns all businesses in that particular location
        # return flask.jsonify({location:businesses})
    else:
        return render_template("view.html")


@app.route('/index.html')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
