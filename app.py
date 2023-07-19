from flask import Flask, request, jsonify
from langchain import OpenAI, ConversationChain, load_tools, initialize_agent
import os

app = Flask(__name__)

# Retrieve the OpenAI API key from an environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Retrieve the SERP API key from an environment variable
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")

# Create an instance of the openAI LLM model
llm = OpenAI(temperature=0.7, api_key=openai_api_key)

# Load necessary tools and initialize an agent with the OpenAI LLM model
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Create an instance of the ConversationChain class
conversation = ConversationChain(llm=llm, verbose=True)

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user input from the request
    user_input = request.json['message']

    # Check if the user input indicates a search query
    if user_input.endswith(":search"):
        # Remove the ":search" suffix from the query
        query = user_input[:-7]

        # Use the agent to perform an internet search
        agent_response = agent.run(query)

        # Return the agent's response as a JSON object
        return jsonify({'search_results': agent_response})

    # Otherwise, use the ConversationChain to generate a response
    response = conversation.predict(input=user_input)

    # Return the response as a JSON object
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run()
