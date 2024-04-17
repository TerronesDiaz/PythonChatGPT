import json
from openai import OpenAI
from config import api_key
import os

class ChatModel:
    # This class is responsible for the logic of the chatbot

    def __init__(self):
        try:
            # Initialize the OpenAI API client
            self.client = OpenAI(api_key=api_key)
            
            # Initialize the messages list with the assistant's initial message
            self.messages = [{"role": "assistant", "content": "I am a helpful assistant created by OpenAI. How can I help you today?"}]
            
            # If the chat history file exists, load it
            if os.path.exists("chat_history.json"):
                with open("chat_history.json", "r") as f:
                    self.messages.extend(json.load(f))
        except Exception as e:
            print(f"Error during initialization: {e}")

    def get_response(self, user_input):
        try:
            # Get the response from the OpenAI API
            self.messages.append({"role": "user", "content": user_input})
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
            )
            response_message = response.choices[0].message.content
            # Add the response to the list of messages
            self.messages.append({"role": "assistant", "content": response_message})

            # Save the chat history
            self.save_chat_history("chat_history.json")

            return response_message
        except Exception as e:
            print(f"Error getting response: {e}")

    # Function to save the chat history
    def save_chat_history(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self.messages, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def reset_chat_history(self):
        try:
            self.messages = [{"role": "assistant", "content": "I am a helpful assistant created by OpenAI. How can I help you today?"}]
            self.save_chat_history("chat_history.json")
            return True
        except Exception as e:
            print(f"Error resetting chat history: {e}")
            return False
