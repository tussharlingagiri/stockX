import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set your Hugging Face token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

# Define the model and the Hugging Face API URL
model_name = "gpt2"  # Use the model you want
api_url = f"https://api-inference.huggingface.co/models/{model_name}"

# Create headers with your token
headers = {
    "Authorization": f"Bearer {os.environ['HUGGINGFACEHUB_API_TOKEN']}",
}

# Function to generate text
def generate_text(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 100,  # Increase max length for more detailed responses
        },
    }
    
    try:
        logging.info(f"Sending request with prompt: {prompt}")
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            logging.info("Received response from Hugging Face API.")
            return response.json()[0]['generated_text']
        else:
            logging.error(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "What is the capital of France?"  # You can modify this prompt
    response_text = generate_text(prompt)
    if response_text:
        print("Response:", response_text)
    else:
        print("No response generated.")
