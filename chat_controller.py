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
        response = self.model.get_response(user_input)
        self.view.display_message(user_input, "user")  
        self.view.display_message(response, "bot") 

    def handle_reset_chat(self):
        self.model.reset_chat_history()
        self.view.text_area.configure(state='normal')
        self.view.text_area.delete(1.0, "end")
        self.view.text_area.configure(state='disabled')
        self.view.display_message("Chat history has been reset.", "bot")

if __name__ == "__main__":
    # Create an instance of the controller and run the chatbot
    controller = ChatController()
    controller.run()
