from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import JsonResponse    
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import json
import pickle

def load_intents():
    try:
        with open('static/intents.json', 'r') as json_file:
            intents = json.load(json_file)
        return intents
    except Exception as e:
        return {"error": f"Failed to load intents: {str(e)}"}
    
def get_symptom_description():
    try:
        descriptions = {}
        with open('static/symptoms_description.json', 'r') as json_file:
            descriptions = json.load(json_file)
            # print(descriptions)
        # Get the description of the predicted symptom
        return descriptions
    except Exception as e:
        return "Error retrieving symptom description: " + str(e)
    
@csrf_exempt
def predict_disease(request):
    if request.method == 'POST':
        symptoms_data = {}
        # Load the symptoms.json file
        with open('static/symptoms.json', 'r') as json_file:
            symptoms_data = json.load(json_file)
        
        # Get the symptoms selected by the user from the request body
        data = json.loads(request.body)
        user_symptoms = data.get('symptoms')  # User's symptoms
        user_symptoms = user_symptoms.split(',')
        
        # Update the symptom dictionary to set the user's symptoms to 1
        for symptom in user_symptoms:
            if symptom in symptoms_data:
                symptoms_data[symptom] = 1

        symptoms_list = list(symptoms_data.keys())
        symptoms_input = [symptoms_data[symptom] for symptom in symptoms_list]

        # Load the pre-trained model
        with open('static/healthcare_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)

        # Reshape the symptom vector to the format required by the model
        symptoms_input = np.array(symptoms_input).reshape(1, -1)

        # Predict the disease using the model 
        predicted_disease = loaded_model.predict(symptoms_input)[0]
        
        # Get a description for the predicted disease (or symptom)
        symptom_description = get_symptom_description()
        description=symptom_description.get(predicted_disease, "Description not available for this symptom.")
        print(description)
        # Return the predicted disease and its description in JSON format
        return JsonResponse({
            'disease': predicted_disease, 
            'description': description
        })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('home')
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # messages.error(request, 'Invalid username or password')
            return JsonResponse({'status': 'error', 'data': 'Invalid username or password'}, status = 400)
    return render(request, 'loginsign.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                # messages.error(request, 'Username already exists')
                return JsonResponse({'status': 'error', 'data': 'Username already exist'}, status=400)
            else:
                User.objects.create_user(username=username, password=password)
                # return redirect('login')
                return JsonResponse({'status': 'success', 'data': 'User registered successfully'}, status=200)
        else:
            # messages.error(request, 'Passwords do not match')
            return JsonResponse({'status': 'error', 'data': 'Password do not match'}, status=400)
    # return render(request, 'register.html')
    
@login_required(login_url='login')
def home(request):
      return render(request, 'home.html')
    
def get_response(user_input):
    # Normalize user input
    user_input = user_input.lower()

    # Responses for common questions, greetings, and health-related topics
    responses = {
        "hi": "Hello! How are you feeling today?",
        "hello": "Hi there! What can I help you with?",
        "thanks": "Glad I could help! Let me know if you need more assistance.",
        "bye": "Take care! If you need me again, I'll be here.",
        "help": "I'm here to assist you. You can ask about symptoms, diseases, or even doctor recommendations.",
        "doctor": "Here are a few doctors I recommend:"
                  "1. Dr. Rahul Sharma - Cardiologist, available at HealthCare Hospital. Contact: +1234567890\n"
                  "2. Dr. Aisha Verma - Dermatologist, SkinCare Clinic. Contact: +0987654321\n"
                  "3. Dr. Vikram Singh - Orthopedic Surgeon, Bone Health Center. Contact: +1122334455\n"
                  "4. Dr. Neha Kapoor - General Physician, Wellness Clinic. Contact: +2233445566",
        "how are you": "I'm just a bot, but I'm always here to help! How about you? How are you feeling?",  
        "what is your name": "I'm your healthcare assistant, always ready to help you with medical advice!",
        "what can you do": "I can help you with information about symptoms, diseases, and even suggest doctors. You can also ask me about common health tips.",
        "common cold treatment": "For common cold, rest and hydration are key. Over-the-counter medicines like paracetamol can help with symptoms. If symptoms persist, consult a doctor.",
        "headache": "Headaches can have many causes. If it’s mild, rest and hydration may help. If it's persistent or severe, consult a healthcare provider.",
        "fever": "For fever, make sure to rest and stay hydrated. You can take medicines like paracetamol to reduce fever. If it’s above 102°F or lasts more than 2 days, contact a doctor.",
        "covid symptoms": "Common COVID-19 symptoms include fever, cough, fatigue, and loss of taste or smell. If you suspect COVID-19, it’s best to get tested and isolate to prevent spreading the virus.",
        "healthy diet": "A balanced diet includes fruits, vegetables, lean proteins, whole grains, and plenty of water. Avoid excessive processed foods, sugar, and salt for better health.",
        "exercise": "Regular exercise like walking, running, or yoga helps maintain fitness and mental well-being. Aim for at least 30 minutes of moderate activity most days of the week.",
        "water intake": "Staying hydrated is important! It's recommended to drink about 8 glasses (2 liters) of water per day, but it can vary depending on your activity level and environment.",
        "stress relief": "To relieve stress, you can try deep breathing exercises, meditation, yoga, or even taking short walks. Regular physical activity and proper sleep are also key!",
        "insomnia": "For better sleep, maintain a consistent sleep schedule, limit screen time before bed, and try relaxation techniques. If insomnia persists, you may want to consult a doctor.",
        "diabetes prevention": "To reduce the risk of diabetes, maintain a healthy weight, stay active, eat a balanced diet, and limit sugar intake. Regular health check-ups are also important.",
        "heart disease prevention": "A healthy lifestyle helps prevent heart disease. Eat a balanced diet, exercise regularly, quit smoking, manage stress, and get regular check-ups."
    }

    # Catch-all response for unknown inputs
    responses["default"] = "I'm not sure how to respond to that. Could you provide more details or clarify your symptoms? Always consider consulting a healthcare provider for accurate diagnosis and treatment."
    
    # Find the right response based on user input
    for key in responses:
        if key in user_input:
            return responses[key]

    # Default response if no match found
    return responses["default"]

# def get_response(user_input):
#     # Load the intents from the JSON file
#     intents = load_intents()

#     if "error" in intents:
#         return intents["error"]

#     user_input = user_input.lower()

#     # Loop through each intent to find a match
#     for intent in intents['intents']:
#         for pattern in intent['text']:
#             if pattern.lower() in user_input:
#                 # If a match is found, return a random response from the intent
#                 return np.random.choice(intent['responses'])

#     # Default response if no intent matches
#     return "Sorry, I don't understand that. Could you rephrase?"

def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        bot_reply = get_response(user_message)
        return JsonResponse({"message": bot_reply})
    return render(request, 'chat.html')
