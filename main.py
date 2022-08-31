# Library Imports
from flask import Flask,jsonify,request
import csv
from encodings import utf_8

# Local Imports
from content_filtering import get_recommendations
from demographic_filtering import output
from storage import all,liked,unliked

all_articles = []

with open('articles.csv', encoding = "utf_8") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]
    
liked_articles = []
unliked_articles = []

app = Flask(__name__)

@app.route("/get-articles")

def get_articles():
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })

@app.route("/liked-articles", methods = ["POST"])

def liked_articles():
    articles = all_articles[0]
    liked_articles.append(articles)

    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-articles", methods = ["POST"])

def unliked_articles():
    movie = all_articles[0]
    unliked_articles.append(movie)

    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")

def popular_articles():
    data_to_return = []

    for i in output:
        data = {
            "url": i[0],
            "title": i[1],
            "text": i[2],
            "lang": i[3],
            "total_events": i[4]
        }

        data_to_return.append(data)

    return jsonify({
        "data": data_to_return,
        "status": "success"
    }) , 201

@app.route("/recommended-articles")

def recommended_articles():
    recommended = []

    for article in liked_articles:
        recommendation = get_recommendations(article[4])

        for data in recommendation:
            recommended.append(data)

    recommended.sort()
    article_data = []
    for data in recommended:
        dictionary = {
            "url": data[0],
            "title": data[1],
            "text": data[2],
            "lang": data[3],
            "total_events": data[4]
        }

        article_data.append(dictionary)


    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
    app.run()