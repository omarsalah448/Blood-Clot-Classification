import requests
import json

def make_prediction(image_path):
    # Specify the URL of your microservice endpoint
    url = 'http://192.168.1.5:5000/predict'
    data = {'image_path': image_path}
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    print("Request sent ... Waiting for a response")
    # Send the POST request to the microservice
    response = requests.post(url, data=json_data, headers=headers)
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        prediction = result['prediction']
        return prediction
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

if __name__ == '__main__':
    image_path = "008e5c_0.tif"
    prediction = make_prediction(image_path)
    if prediction is not None:
        print("Prediction:", prediction)
