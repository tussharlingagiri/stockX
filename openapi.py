import openai
import time

openai.api_key = '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'

prompt = "What is the capital of France?"
max_retries = 5  # Maximum number of retries
retry_delay = 1  # Initial delay in seconds

for attempt in range(max_retries):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        print(response['choices'][0]['message']['content'])
        break  # Exit the loop if the request is successful
    except openai.error.RateLimitError:
        print(f"Rate limit exceeded. Waiting for {retry_delay} seconds...")
        time.sleep(retry_delay)
        retry_delay *= 2  # Double the wait time for the next attempt
    except Exception as e:
        print(f"An error occurred: {e}")
        break  # Exit the loop on any other error
else:
    print("Max retries exceeded. Please check your API usage and try again later.")
