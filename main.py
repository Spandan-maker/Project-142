from flask import Flask, jsonify, request
from flask_cors import CORS
from storage import all_articles, liked_articles, unliked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)
CORS(app)

@app.route("/get-articles")
def get_articles():
    article_details = {
        'title': all_articles[0][12],
        'url': all_articles[0][11],
        'text': all_articles[0][13]
    }
    return jsonify({
        "Data" : article_details,
        "status" : "Success"
    })

@app.route("/liked-articles", methods = ["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)

    return jsonify({
        "status": "Sucess"
    }), 201

@app.route("/unliked-articles", methods = ["POST"])
def unliked_article():
    article = all_articles[0]
    unliked_articles.append(article)
    all_articles.pop(0)

    return jsonify({
        "status": "Sucess"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "content_id": article[1],
            "author_person_id": article[2],
            "url": article[3] or "N/A"
        }
        article_data.append(_d)
    return jsonify({
        "Data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[12])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "url": recommended[1],
            "content_id": recommended[2] or "N/A",
            "author_person_id": recommended[3]
        }
        movie_data.append(_d)
    return jsonify({
        "Data": movie_data,
        "status": "success"
    }), 200


if __name__ == "__main__":
    app.run()
