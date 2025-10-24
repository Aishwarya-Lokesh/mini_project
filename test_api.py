import requests

# Example user data
user_data = {
    "age": 28,
    "weight": 70,
    "height": 175,
    "bmi": 22.9,
    "goal": "Lose",
    "health_condition": "None",
    "activity_level": "Moderate"
}

# Send POST request
response = requests.post("http://localhost:5001/predict", json=user_data)

# Print the result
print(response.json())
