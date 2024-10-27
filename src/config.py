import os

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = 'XM14CD2Y9TOP177V'

# Hugging Face API Token
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN', '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')

# Hugging Face Model URL
HUGGINGFACE_MODEL_NAME = "gpt2"
HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL_NAME}"
