from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

# Load data and models
top50Books = pickle.load(open('data/top50books.pkl', 'rb'))
pt = pickle.load(open('data/pt.pkl', 'rb'))
books = pickle.load(open('data/books.pkl', 'rb'))
similarity_scores = pickle.load(open('data/similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html',
                           book_title=list(top50Books['Book-Title'].values),
                           author=list(top50Books['Book-Author'].values),
                           rating=list(top50Books['Avg-Rating'].values),
                           image=list(top50Books['Image-URL-M'].values),
                           votes=list(top50Books['No-Ratings'].values))


@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')


@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]  # Get top 5 recommendations

        recommendations = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            if not temp_df.empty:
                book_data = {
                    "title": temp_df['Book-Title'].values[0],
                    "author": temp_df['Book-Author'].values[0],
                    "image": temp_df['Image-URL-M'].values[0]
                }
                recommendations.append(book_data)

        return render_template('recommendation.html',
                               user_input=user_input,
                               recommendations=recommendations)
    except IndexError:
        return render_template('recommendation.html',
                               error="Book not found. Please try another title.")


# API endpoint for recommendations
@app.route('/api/recommend_books', methods=['POST'])
def api_recommend_books():
    data = request.json
    user_input = data.get('book_title', '')
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        recommendations = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            if not temp_df.empty:
                book_data = {
                    "title": temp_df['Book-Title'].values[0],
                    "author": temp_df['Book-Author'].values[0],
                    "image": temp_df['Image-URL-M'].values[0]
                }
                recommendations.append(book_data)

        return jsonify({"status": "success", "recommendations": recommendations})
    except IndexError:
        return jsonify({"status": "error", "message": "Book not found"})


# API endpoint for top 50 books
@app.route('/api/top50_books', methods=['GET'])
def api_top50_books():
    try:
        books_data = []
        for _, row in top50Books.iterrows():
            books_data.append({
                "title": row['Book-Title'],
                "author": row['Book-Author'],
                "rating": row['Avg-Rating'],
                "image": row['Image-URL-M'],
                "votes": row['No-Ratings']
            })

        return jsonify({"status": "success", "top_books": books_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
