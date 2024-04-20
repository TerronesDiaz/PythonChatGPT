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
        self.view.display_message(response, "bot")  


    def handle_reset_chat(self):
        self.model.reset_chat_history()
        
        # Clear the canvas instead of text_area
        self.view.canvas.delete("text")  
        self.view.canvas.delete("image")  

        # Reset the last_message_bottom to its initial value
        self.view.last_message_bottom = 5
        
        # Update the scrollregion after clearing the canvas
        self.view.canvas.configure(scrollregion=self.view.canvas.bbox("all"))
        
        # Display a message indicating that the chat has been reset
        self.view.display_message("Chat history has been reset.", "bot")


if __name__ == "__main__":
    # Create an instance of the controller and run the chatbot
    controller = ChatController()
    controller.run()
