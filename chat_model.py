from openai import OpenAI
from config import api_key

class ChatModel:
    # This class is responsible for the logic of the chatbot

    def __init__(self):
        # Initialize the OpenAI API client
        self.client = OpenAI(api_key=api_key)
        self.messages = [{"role": "system", "content": "I am a helpful assistant created by OpenAI. How can I help you today?"}]

    def get_response(self, user_input):
        # Get the response from the OpenAI API
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        response_message = response.choices[0].message.content
        # Add the response to the list of messages
        self.messages.append({"role": "assistant", "content": response_message})
        return response_message
