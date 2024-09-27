
# HealthCare Chatbot

A healthcare chatbot designed to provide users with quick and accurate responses related to their health queries, including symptom analysis, disease prediction, and doctor recommendations. Built using Django, React, Rasa, and a machine learning model for disease prediction.

## Features

* **Symptom Prediction**: Users can input symptoms, and the bot predicts potential diseases.
* **Disease Information**: After predicting a disease, the chatbot provides a detailed description of the disease.
* **Doctor Suggestions**: The bot can suggest doctors based on the user's query.
* **User Authentication**: Secure login and signup forms for managing user accounts.
* **Interactive Chat Interface**: A responsive and user-friendly interface for seamless interaction.

## Tech Stack

* **Backend**: Django
* **Frontend**: React.js
* **Machine Learning**: RandomForestClassifier (for disease prediction)
* **Chatbot Framework**: Rasa
* **Database**: SQLite (or PostgreSQL/MySQL for production)
* **Styling**: CSS, Flexbox layout for responsive design

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/healthcare-chatbot.git
   cd healthcare-chatbot
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

* **Access the chatbot**: Once the server is running, go to `http://localhost:8000/chat` to interact with the chatbot.
* **Admin Panel**: Visit `http://localhost:8000/admin` for managing users, chatbot models, etc.
* **User Account**: Create an account or log in to access personalized chatbot responses.

## Project Structure

```bash
/healthcare-chatbot
├── /chatbot                # Contains Rasa chatbot configurations and ML models
├── /static                 # Static files (CSS, JS, images)
├── /templates              # HTML templates for the frontend
├── /app1                   # Django app containing views, models, etc.
├── /node_modules           # React dependencies
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Machine Learning Model

* **RandomForestClassifier** is used to predict diseases based on the symptoms provided by users.
* The model is trained using healthcare data and integrated with the chatbot for real-time predictions.

## Contributions

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
