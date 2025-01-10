
# Flask Book Recommendation System

This repository contains a Flask-based application that provides a book recommendation system. The app uses algorithms to recommend similar books based on user input and includes APIs for testing and integration.

## Features

- Display top 50 books with their details.
- Recommend books based on user input using similarity scores.
- RESTful API endpoints for fetching recommendations and top books.
- Secure API access with an API key.

## Technologies Used

- Flask
- Python
- NumPy
- Pandas
- Pickle (for model and data storage)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/mrravipandee/flask-book-recommendation-system.git
   cd flask-book-recommendation-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place the required data files (`top50books.pkl`, `pt.pkl`, `books.pkl`, `similarity_scores.pkl`) in the `data/` directory.

5. Add your API key to the `.env` file:
   ```plaintext
   API_KEY=your-secure-api-key
   ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

7. Access the application in your browser at `http://127.0.0.1:5000`.

## API Endpoints

### 1. Get Book Recommendations
- **URL**: `/api/recommend_books`
- **Method**: `POST`
- **Headers**: `{ "API-Key": "your-api-key" }`
- **Body**: `{ "book_title": "example book title" }`
- **Response**:
  ```json
  {
    "status": "success",
    "recommendations": [
      {
        "title": "Book Title",
        "author": "Author Name",
        "image": "Image URL"
      },
      ...
    ]
  }
  ```

### 2. Get Top 50 Books
- **URL**: `/api/top50_books`
- **Method**: `GET`
- **Headers**: `{ "API-Key": "your-api-key" }`
- **Response**:
  ```json
  {
    "status": "success",
    "top_books": [
      {
        "title": "Book Title",
        "author": "Author Name",
        "rating": "Average Rating",
        "image": "Image URL",
        "votes": "Number of Ratings"
      },
      ...
    ]
  }
  ```

## Author

- **Email**: [imravipanday@gmail.com](mailto:imravipanday@gmail.com)
- **X (formerly Twitter)**: [@mrravipandee](https://x.com/mrravipandee)
- **GitHub**: [mrravipandee](https://github.com/mrravipandee)

---

Feel free to fork the repository, raise issues, or contribute to improve this project!
