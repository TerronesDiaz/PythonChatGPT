from chat_model import ChatModel
from chat_view import ChatView

class ChatController:
    # This class is responsible for the interaction between the model and the view

    def __init__(self):
        # Initialize the model and view
        self.model = ChatModel()
        self.view = ChatView(self)

    def run(self):
        # Run the main event loop
        self.view.mainloop()

    def handle_user_input(self, user_input):
        # Get the response from the model and display it in the view
        response = self.model.get_response(user_input)
        self.view.display_message(f"You: {user_input}")
        self.view.display_message(f"ChatBot: {response}")

if __name__ == "__main__":
    # Create an instance of the controller and run the chatbot
    controller = ChatController()
    controller.run()
