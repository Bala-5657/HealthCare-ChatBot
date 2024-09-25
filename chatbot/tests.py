from django.test import TestCase

# Create your tests here.


import pickle

file_path = 'healthcare_chatbot_model.pkl'

try:
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    print(data)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except pickle.UnpicklingError:
    print("Error: The file content is not a valid pickle format.")
except EOFError:
    print("Error: The file is incomplete or corrupted.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# Step 2: Write the data to a .txt file
with open('data.txt', 'w') as txt_file:
    txt_file.write(str(data))
