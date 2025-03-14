from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pickle
import numpy as np
import random
import string
import nltk
import re
import os
from gtts import gTTS
from nltk.sentiment import SentimentIntensityAnalyzer

# Load necessary data and models
top50Books = pickle.load(open('./data/top50books.pkl', 'rb'))
pt = pickle.load(open('./data/pt.pkl', 'rb'))
books = pickle.load(open('./data/books.pkl', 'rb'))
similarity_scores = pickle.load(open('./data/similarity_scores.pkl', 'rb'))

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)
CORS(app)

API_KEY = "X7b!9aY@ZP#2kM^NcT*5wVJ&8LrQ%X4G"


def authenticate_request():
    """Check API key authentication."""
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized access, invalid API key."}), 401


@app.route('/')
def home():
    return render_template('index.html',
                           book_title=top50Books['Book-Title'].tolist(),
                           author=top50Books['Book-Author'].tolist(),
                           rating=top50Books['Avg-Rating'].tolist(),
                           image=top50Books['Image-URL-M'].tolist(),
                           votes=top50Books['No-Ratings'].tolist())


@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')


@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0]

    if index.size == 0:
        return render_template('recommendation.html', error="Book not found. Please try another title.")

    similar_items = sorted(enumerate(similarity_scores[index[0]]), key=lambda x: x[1], reverse=True)[1:6]
    recommendations = [{
        "title": books.loc[books['Book-Title'] == pt.index[i[0]], 'Book-Title'].values[0],
        "author": books.loc[books['Book-Title'] == pt.index[i[0]], 'Book-Author'].values[0],
        "image": books.loc[books['Book-Title'] == pt.index[i[0]], 'Image-URL-M'].values[0]
    } for i in similar_items if not books[books['Book-Title'] == pt.index[i[0]]].empty]

    return render_template('recommendation.html', user_input=user_input, recommendations=recommendations)


@app.route('/api/recommend_books', methods=['POST'])
def api_recommend_books():
    data = request.json
    user_input = data.get('book_title', '')
    index = np.where(pt.index == user_input)[0]

    if index.size == 0:
        return jsonify({"status": "error", "message": "Book not found"})

    similar_items = sorted(enumerate(similarity_scores[index[0]]), key=lambda x: x[1], reverse=True)[1:6]
    recommendations = [{
        "title": books.loc[books['Book-Title'] == pt.index[i[0]], 'Book-Title'].values[0],
        "author": books.loc[books['Book-Title'] == pt.index[i[0]], 'Book-Author'].values[0],
        "image": books.loc[books['Book-Title'] == pt.index[i[0]], 'Image-URL-M'].values[0]
    } for i in similar_items if not books[books['Book-Title'] == pt.index[i[0]]].empty]

    return jsonify({"status": "success", "recommendations": recommendations})


@app.route('/api/top50_books', methods=['GET'])
def api_top50_books():
    books_data = top50Books.to_dict(orient='records')
    return jsonify({"status": "success", "top_books": books_data})


@app.route('/api/get_book_image', methods=['POST'])
def get_book_image():
    data = request.json
    book_title = data.get('book_title', '')
    book_data = books[books['Book-Title'] == book_title]

    if book_data.empty:
        return jsonify({"status": "error", "message": "Book not found"})

    return jsonify({"status": "success", "image_url": book_data['Image-URL-M'].values[0]})


@app.route('/api/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    text = request.json.get("text", "")
    if not text:
        return jsonify({"status": "error", "message": "Text input required"})

    sentiment_score = sia.polarity_scores(text)["compound"]
    sentiment = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
    return jsonify({"status": "success", "sentiment": sentiment, "score": sentiment_score})


@app.route('/api/abusive_detection', methods=['POST'])
def abusive_detection():
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    abusive_words = {"badword1", "badword2", "offensiveword"}  # Expand as needed
    text = request.json.get("text", "")
    if not text:
        return jsonify({"status": "error", "message": "Text input required"})

    is_abusive = bool(set(re.findall(r"\w+", text.lower())) & abusive_words)
    return jsonify({"status": "success", "abusive": is_abusive})


@app.route("/api/text_to_speech", methods=["POST"])
def text_to_speech():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"status": "error", "message": "Text input required"})

    tts = gTTS(text)
    filename = "output.mp3"
    file_path = os.path.join("static", filename)  # Store in a static folder
    tts.save(file_path)

    return jsonify({
        "status": "success",
        "message": "Text converted to speech.",
        "download_url": f"/download/output.mp3"
    })

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join("static", filename)
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    print(f"Generated API Key: {API_KEY}")  # Store this securely
    app.run(debug=True)
