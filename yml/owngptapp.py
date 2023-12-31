import os
import openai
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a variable to track the timestamp of the last API call
last_call_time = time.time()

# Define the rate limit (in seconds)
rate_limit = 60 / 3  # 3 RPM

# Create a while loop that runs until the user types 'exit'
while True:
    # Check if enough time has passed since the last API call
    if time.time() - last_call_time < rate_limit:
        # Wait for the remaining time before making the next API call
        time.sleep(rate_limit - (time.time() - last_call_time))

    # Gets input from the user to ask a question (blue text)
    question = input("\033[34mWhat is your question?\n\033[0m")

    # Checks if the user entered 'exit'
    if question.lower() == "exit":
        # Breaks the loop and prints a goodbye message (red text)
        print("\033[31mGoodbye!\033[0m")
        break

    # Uses the openai.ChatCompletion.create() method to generate a response to the question
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer the given question."},
            {"role": "user", "content": question}
        ]
    )

    # Update the last call time with the current timestamp
    last_call_time = time.time()

    # Prints the response generated by the AI (green text)
    print("\033[32m" + completion.choices[0].message.content + "\n")

    



