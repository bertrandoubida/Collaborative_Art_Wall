# Art Wall Project

This project is a Flask-based web application that allows users to create a collaborative "art wall." Users can submit messages, which are stored temporarily using Momento, and all messages are displayed dynamically on a shared canvas.

## Features
- **Message Submission:** Users can submit messages via an API endpoint.
- **Dynamic Display:** Messages are shown on a canvas in randomized colors, font sizes, positions, and angles.
- **Temporary Storage:** Messages are cached for 6 hours using Momento, ensuring a fresh and evolving art wall.
- **API Integration:** Fully functional API endpoints for adding and retrieving messages.

## Requirements
- Python 3.9+
- Flask
- Momento SDK
- dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd art-wall-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following:
     ```plaintext
     MOMENTO_API_KEY=your_momento_api_key_here
     CACHE_NAME=art_wall
     ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Access the application:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## API Endpoints
### Add a Message
**POST** `/add-message`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "message": "Your message here"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Message added successfully!"
  }
  ```

### Get All Messages
**GET** `/get-messages`
- **Response:**
  ```json
  {
    "messages": [
      "Hello, Art Wall!",
      "Another message"
    ]
  }
  ```

## Notes
- **Caching:** Messages are stored in the Momento cache and expire after 6 hours.
- **Error Handling:** Handles missing keys or cache errors gracefully.

## Testing
1. Use Postman, `cURL`, or a Python HTTP library to test the API.
2. Example `cURL` commands:
   ```bash
   # Add a message
   curl -X POST http://127.0.0.1:5000/add-message \
   -H "Content-Type: application/json" \
   -d '{"message": "Test message"}'

   # Get all messages
   curl -X GET http://127.0.0.1:5000/get-messages
   ```

## Future Enhancements
- User authentication for personalized submissions.
- Advanced canvas animations.
- Support for longer storage durations or persistence options.

---
For any issues or suggestions, feel free to reach out!

