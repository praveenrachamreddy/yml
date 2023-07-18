from flask import Flask, request, jsonify
from langchain.llms import openAI
from langchain import ConversationChain
from serpapi import GoogleSearch
import os

app = Flask(__name__)

# Retrieve the OpenAI API key from an environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Retrieve the SERP API key from an environment variable
serpapi_api_key = os.environ.get("SERPAPI_API_KEY")

# Create an instance of the openAI LLM model
llm = openAI(temperature=0.7, api_key=openai_api_key)

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
        
        # Perform a Google search using SERP API
        search_results = perform_google_search(query)
        
        # Return the search results as a JSON object
        return jsonify({'search_results': search_results})
    
    # Otherwise, use the ConversationChain to generate a response
    response = conversation.predict(input=user_input)

    # Return the response as a JSON object
    return jsonify({'message': response})

def perform_google_search(query):
    params = {
        "api_key": serpapi_api_key,
        "engine": "google",
        "q": query
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    search_results = []
    for result in results['organic_results']:
        search_results.append({
            'title': result['title'],
            'link': result['link']
        })

    return search_results

if __name__ == '__main__':
    app.run()


#docker run -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key -e SERPAPI_API_KEY=your_serpapi_api_key chatbot-app
