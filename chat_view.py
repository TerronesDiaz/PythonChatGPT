import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from better_profanity import profanity
from PIL import Image, ImageTk, ImageDraw
import json
import os
import base64
from io import BytesIO

class ChatView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.user_image_positions = {}  # Track positions and their marks
        self.load_config()
        self.bot_image = ImageTk.PhotoImage(Image.open("bot.png").resize((50, 50)))
        self.setup_ui()
        self.load_and_display_messages()
    
    def load_and_display_messages(self):
        # This method will load and display historical messages from the model
        messages = self.controller.model.get_messages()
        for message in messages:
            if message['role'] == 'user':
                self.display_message(message['content'], "user")
            elif message['role'] == 'assistant':
                self.display_message(message['content'], "bot")
        self.display_message("Ready to assist you. How can I help today?", "bot")

    def create_round_image(self, img, size=(50, 50)):
        img = img.resize(size, Image.LANCZOS)
        mask = Image.new('L', img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)
        return img

    def load_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                user_image_data = config.get('user_image')
                if user_image_data:
                    user_image = Image.open(BytesIO(base64.b64decode(user_image_data)))
                    rounded_image = self.create_round_image(user_image)
                    self.user_image_raw = ImageTk.PhotoImage(rounded_image)
                else:
                    default_img = Image.open('user.png')
                    rounded_image = self.create_round_image(default_img)
                    self.user_image_raw = ImageTk.PhotoImage(rounded_image)
        else:
            default_img = Image.open('user.png')
            rounded_image = self.create_round_image(default_img)
            self.user_image_raw = ImageTk.PhotoImage(rounded_image)
        self.user_image = self.user_image_raw

    def save_config(self, image):
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        with open('config.json', 'w') as f:
            json.dump({'user_image': image_data}, f)

    def setup_ui(self):
        self.title("OpenAI Chatbot")
        self.geometry("800x600")  # Adjusted for typical screen size

        self.chat_frame = tk.Frame(self)
        self.chat_frame.grid(row=0, column=0, columnspan=5, sticky='nsew')

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, state='disabled', wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry_message = ttk.Entry(self)
        self.entry_message.grid(row=1, column=0, sticky='ew')
        self.entry_message.focus()

        send_button = ttk.Button(self, text="Send", command=self.on_send)
        send_button.grid(row=1, column=1, sticky='ew')

        #reset button
        reset_button = ttk.Button(self, text="Reset Chat", command=self.on_reset_chat)
        reset_button.grid(row=1, column=4, sticky='ew')

        quit_button = ttk.Button(self, text="Quit", command=self.on_quit)
        quit_button.grid(row=1, column=2, sticky='ew')

        change_image_button = ttk.Button(self, text="Change Photo", command=self.change_photo)
        change_image_button.grid(row=1, column=3, sticky='ew')

        self.entry_message.bind("<Return>", lambda event: self.on_send())

    def on_send(self):
        user_input = self.entry_message.get()
        if user_input and not profanity.contains_profanity(user_input):
            self.controller.handle_user_input(user_input)
            self.entry_message.delete(0, tk.END)
        elif profanity.contains_profanity(user_input):
            messagebox.showwarning("Warning", "Please refrain from using inappropriate language.")
            self.entry_message.delete(0, tk.END)

    def on_reset_chat(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the chat history?"):
            self.controller.handle_reset_chat()

    def display_message(self, message, sender):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, "\n")
        if sender == "user":
            image_to_use = self.user_image
            self.text_area.image_create(tk.END, image=image_to_use, padx=10, pady=10)
        else:
            image_to_use = self.bot_image
            self.text_area.image_create(tk.END, image=image_to_use, padx=10, pady=10)
        self.text_area.insert(tk.END, " " + message + "\n")
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def change_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            new_image = Image.open(file_path)
            rounded_image = self.create_round_image(new_image)
            self.user_image_raw = ImageTk.PhotoImage(rounded_image)
            self.save_config(new_image)
            messagebox.showinfo("Success", "Photo changed successfully.")
            self.update_all_user_images()

    def update_all_user_images(self):
        """Update all displayed user images in the text area."""
        self.user_image = self.user_image_raw  
        for index in self.text_area.tag_names():
            if "user_image" in index:
                self.text_area.tag_config(index, image=self.user_image)

    def on_quit(self):
        if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?"):
            self.destroy()