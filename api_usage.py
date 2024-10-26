import os
import requests

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
            "max_length": 50,
        },
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        print("Error:", response.status_code, response.text)
        return None

# Example usage
response_text = generate_text("What is the capital of France?")
print(response_text)
