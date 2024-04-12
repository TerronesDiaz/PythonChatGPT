import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox  # Importa messagebox

class ChatView(tk.Tk):
    # This class is responsible for the GUI of the chatbot

    def __init__(self, controller):
        # Initialize the main window
        super().__init__()
        self.controller = controller
        # Customizing the main window
        self.title("OpenAI Chatbot")
        self.geometry("500x400")
        self.text_area = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.entry_message = ttk.Entry(self)
        self.entry_message.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.entry_message.focus()
        # Greet the user
        self.display_message("I am a helpful assistant, how can I help you today?")

        # Bind the Enter key to the send message function
        self.entry_message.bind("<Return>", lambda e: self.on_send())

        # Create the send and quit buttons
        self.send_button = ttk.Button(self, text="Send", command=self.on_send)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.quit_button = ttk.Button(self, text="Quit", command=self.confirm_quit)  # Cambiado para llamar a confirm_quit
        self.quit_button.grid(row=1, column=2, padx=5, pady=5)
        
        #Create the help button
        self.help_button = ttk.Button(self, text="Help", command=self.help)
        self.help_button.grid(row=1, column=3, padx=5, pady=5)

    def on_send(self):
        # Get the user input and handle it
        user_input = self.entry_message.get()
        if user_input:
            self.controller.handle_user_input(user_input)
            self.entry_message.delete(0, tk.END)

    def display_message(self, message):
        # Display a message in the text area
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.configure(state='disabled')

    def confirm_quit(self): 
        # Confirm if the user wants to quit
        if messagebox.askyesno("Confirm", "Are you sure you want to quit?"):
            self.quit()

    def help(self):
        # Display a help message
        messagebox.showinfo("Help", "This is a chatbot created by OpenAI. You can chat with me by typing your message in the input box and pressing the Send button. If you want to quit, press the Quit button.")
