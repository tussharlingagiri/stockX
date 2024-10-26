import openai
import time
import logging

# Set your OpenAI API key
openai.api_key = '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'

# Configure logging
logging.basicConfig(level=logging.INFO)

def ask_openai(prompt):
    max_retries = 5  # Maximum number of retries
    base_delay = 1  # Initial delay in seconds
    requests_made = 0  # Counter for API requests

    for attempt in range(max_retries):
        try:
            requests_made += 1  # Increment request counter
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            logging.info(f"Requests made: {requests_made}")  # Log requests made
            return response['choices'][0]['message']['content']
        except openai.error.RateLimitError:
            delay = base_delay * (2 ** attempt)  # Exponential backoff
            logging.warning(f"Rate limit exceeded. Waiting for {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break
    else:
        logging.error("Max retries exceeded. Please check your API usage and try again later.")

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    answer = ask_openai(prompt)
    if answer:
        print(f"Answer: {answer}")
