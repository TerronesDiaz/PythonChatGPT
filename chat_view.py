import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from better_profanity import profanity
from PIL import Image, ImageTk

class ChatView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.bot_image = ImageTk.PhotoImage(Image.open("bot.png").resize((50, 50)))
        self.user_image = ImageTk.PhotoImage(Image.open("user.png").resize((50, 50)))
        self.setup_ui()
        self.display_message("ChatBot: I am a helpful assistant created by OpenAI. How can I help you today?", "bot")

    def setup_ui(self):
        self.title("OpenAI Chatbot")
        self.geometry("800x800")

        self.chat_frame = tk.Frame(self)
        self.chat_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry_message = ttk.Entry(self)
        self.entry_message.grid(row=1, column=0, sticky='ew')
        self.entry_message.focus()

        send_button = ttk.Button(self, text="Send", command=self.on_send)
        send_button.grid(row=1, column=1, sticky='ew')

        quit_button = ttk.Button(self, text="Quit", command=self.on_quit)
        quit_button.grid(row=1, column=2, sticky='ew')

        self.entry_message.bind("<Return>", lambda event: self.on_send())

    def on_send(self):
        user_input = self.entry_message.get()
        if user_input and not profanity.contains_profanity(user_input):
            self.controller.handle_user_input(user_input)  # Let the controller manage displaying messages
            self.entry_message.delete(0, tk.END)
        elif profanity.contains_profanity(user_input):
            messagebox.showwarning("Warning", "Please refrain from using inappropriate language.")
            self.entry_message.delete(0, tk.END)


    def display_message(self, message, sender):
        self.text_area.configure(state='normal')
        image_to_use = self.bot_image if sender == "bot" else self.user_image
        self.text_area.image_create(tk.END, image=image_to_use)
        self.text_area.insert(tk.END, f" {message}\n")
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')



    def on_quit(self):
        if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?"):
            self.destroy()
