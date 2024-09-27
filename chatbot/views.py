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
    
    "common cold": "The common cold is a viral infection that affects the nose and throat, causing symptoms like a runny nose, cough, and sore throat.",
    "remedy for common cold": "Rest, stay hydrated, and take over-the-counter cold medications. Symptoms typically resolve in a few days, but consult a doctor if they persist.",
    
    "fever": "Fever is an elevated body temperature, usually a sign of an underlying infection or illness.",
    "remedy for fever": "Stay hydrated, rest, and take over-the-counter medications like paracetamol to lower the temperature. If the fever is above 102°F or lasts more than a couple of days, see a doctor.",

    "headache": "Headaches can have many causes, ranging from dehydration to stress or more serious conditions.",
    "remedy for headache": "Stay hydrated, rest in a quiet and dark room, and take over-the-counter pain relief if necessary. If the headache is persistent or severe, consult a doctor.",

    "covid-19": "COVID-19 is a viral infection caused by the SARS-CoV-2 virus, with symptoms ranging from mild (cough, fever) to severe (difficulty breathing).",
    "remedy for covid-19": "Isolate yourself, stay hydrated, and follow medical advice. Over-the-counter medications may alleviate symptoms, but severe cases require immediate medical care.",

    "allergy": "Allergies occur when your immune system reacts to foreign substances like pollen, pet dander, or certain foods.",
    "remedy for allergy": "Identify and avoid the allergen. Antihistamines can help alleviate symptoms. For severe reactions, seek medical attention immediately.",

    "asthma": "Asthma is a chronic condition that causes the airways to narrow and swell, making breathing difficult.",
    "remedy for asthma": "Use prescribed inhalers, avoid triggers such as dust and smoke, and follow your doctor’s asthma management plan.",

    "diabetes": "Diabetes affects your body’s ability to regulate blood sugar, leading to high blood sugar levels.",
    "remedy for diabetes": "Maintain a balanced diet, engage in regular physical activity, monitor blood glucose levels, and take prescribed medications. Regular check-ups with a doctor are crucial.",

    "hypertension": "Hypertension, or high blood pressure, increases the risk of heart disease and stroke.",
    "remedy for hypertension": "Adopt a heart-healthy diet low in salt, exercise regularly, manage stress, and take medications as prescribed.",

    "migraine": "A migraine is a severe, recurring headache that is often accompanied by nausea, sensitivity to light, and throbbing pain.",
    "remedy for migraine": "Rest in a dark, quiet room, apply cold compresses, and use over-the-counter or prescription medications. Preventive treatments may be necessary for frequent migraines.",

    "bronchial asthma": "Bronchial asthma leads to episodes of wheezing, chest tightness, and shortness of breath due to inflamed airways.",
    "remedy for bronchial asthma": "Keep a rescue inhaler on hand, avoid known triggers, and follow your asthma action plan. Long-term control medications may be needed if attacks are frequent.",

    "pneumonia": "Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus.",
    "remedy for pneumonia": "Rest, take prescribed antibiotics or antiviral medications, stay hydrated, and seek immediate medical attention if symptoms become severe.",

    "hepatitis": "Hepatitis refers to inflammation of the liver, often caused by viral infections or excessive alcohol consumption.",
    "remedy for hepatitis": "Rest, follow your doctor's advice, and avoid alcohol and other substances that could harm the liver. Antiviral medications may be needed in some cases.",

    "tuberculosis": "Tuberculosis (TB) is a contagious bacterial infection that primarily affects the lungs but can spread to other organs.",
    "remedy for tuberculosis": "Complete the full course of antibiotics, typically lasting six to nine months. Regular follow-up with your healthcare provider is essential.",

    "peptic ulcer": "Peptic ulcers are sores that develop on the inner lining of your stomach or the upper part of your small intestine, often due to H. pylori infection or prolonged use of NSAIDs.",
    "remedy for peptic ulcer": "Avoid spicy foods, alcohol, and NSAIDs. Take prescribed medications such as proton pump inhibitors (PPIs) to reduce stomach acid and allow the ulcer to heal.",

    "urinary tract infection": "UTIs are infections in any part of the urinary system, including the kidneys, bladder, and urethra, often caused by bacteria.",
    "remedy for urinary tract infection": "Drink plenty of water, take prescribed antibiotics, and urinate frequently to flush out bacteria. Consult a doctor if symptoms persist or worsen.",

    "arthritis": "Arthritis is inflammation of the joints, causing pain, stiffness, and reduced movement. There are many types, including osteoarthritis and rheumatoid arthritis.",
    "remedy for arthritis": "Maintain regular physical activity, use pain relief or anti-inflammatory medications, and consider physical therapy for joint support. Severe cases may require stronger medications or surgery.",

    "dengue": "Dengue fever is a viral infection spread by mosquitoes, causing high fever, rash, and muscle/joint pain. In severe cases, it can lead to hemorrhagic fever or shock.",
    "remedy for dengue": "Rest, hydrate, and avoid nonsteroidal anti-inflammatory drugs (NSAIDs) like aspirin. Seek immediate medical care if symptoms become severe, such as bleeding or difficulty breathing.",

    "gastroenteritis": "Gastroenteritis, often called the stomach flu, is inflammation of the stomach and intestines, leading to diarrhea, vomiting, and cramps.",
    "remedy for gastroenteritis": "Rest, stay hydrated with water or oral rehydration solutions, and avoid solid food until symptoms improve. Consult a doctor if symptoms persist or worsen.",

    "heart attack": "A heart attack occurs when blood flow to the heart is blocked, causing damage to heart muscle tissue.",
    "remedy for heart attack": "Call emergency services immediately. Take aspirin if advised by a doctor, and stay calm. Treatment in a hospital will include restoring blood flow to the heart.",

    "bronchitis": "Bronchitis is inflammation of the bronchial tubes, causing coughing, mucus production, and shortness of breath.",
    "remedy for bronchitis": "Rest, increase fluid intake, and avoid irritants like smoke. Over-the-counter medications can help with symptoms, but consult a doctor if it becomes chronic.",

    "chickenpox": "Chickenpox is a highly contagious viral infection causing an itchy rash and flu-like symptoms.",
    "remedy for chickenpox": "Rest, apply calamine lotion to soothe itching, and avoid scratching. Antiviral medication may be needed in severe cases.",

    "jaundice": "Jaundice is a condition where the skin and whites of the eyes turn yellow due to high bilirubin levels, often caused by liver issues.",
    "remedy for jaundice": "Follow your doctor’s advice, which may include dietary changes, medications, or treatment for the underlying condition causing jaundice.",

    "healthy diet": "A balanced diet includes fruits, vegetables, lean proteins, whole grains, and plenty of water. Avoid excessive processed foods, sugar, and salt for better health.",
    "exercise": "Regular exercise like walking, running, or yoga helps maintain fitness and mental well-being. Aim for at least 30 minutes of moderate activity most days of the week.",
    "water intake": "Staying hydrated is important! It's recommended to drink about 8 glasses (2 liters) of water per day, but it can vary depending on your activity level and environment.",
    "stress relief": "To relieve stress, you can try deep breathing exercises, meditation, yoga, or even taking short walks. Regular physical activity and proper sleep are also key!",
    "insomnia": "For better sleep, maintain a consistent sleep schedule, limit screen time before bed, and try relaxation techniques. If insomnia persists, consult a healthcare provider.",
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
