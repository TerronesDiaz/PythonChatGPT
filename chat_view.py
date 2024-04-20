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
        self.last_message_bottom = 5
        self.user_image_positions = {}  # Track positions and their marks
        self.load_config()
        self.bot_image = ImageTk.PhotoImage(
            Image.open("bot.png").resize((50, 50)))
        self.setup_ui()
        self.load_and_display_messages()
        self.canvas.bind('<Configure>', self.on_canvas_resize)

    def on_canvas_resize(self, event):
        """
        This function repositions and resizes image-text pairs within the canvas when the canvas is resized.

        Args:
            event: The event object that triggers the function call.

        Returns:
            None
        """

        # Get the new width of the canvas
        canvas_width = event.width

        # Set the initial bottom margin for the first message
        last_bottom = 5

        # Retrieve all image and text objects from the canvas
        images = self.canvas.find_withtag("image")
        texts = self.canvas.find_withtag("text")

        # Pair up the image and text objects
        image_text_pairs = list(zip(images, texts))

        # Sort the image-text pairs by their Y coordinates (top-to-bottom)
        sorted_image_text_pairs = sorted(
            image_text_pairs, key=lambda x: self.canvas.coords(x[0])[1])

        # Iterate through the sorted image-text pairs
        for image_id, text_id in sorted_image_text_pairs:

            # Set the initial X position for the image
            img_x = 5

            # Calculate the Y position for the image based on the last bottom margin
            img_y = last_bottom + 10

            # Reposition the image
            self.canvas.coords(image_id, (img_x, img_y))

            # Set up configuration for the text
            # X position after the image
            text_x = self.canvas.bbox(image_id)[2] + 10
            text_y = img_y + 15  # Align Y with the image with a slight offset below

            # Determine the available width for the text
            text_width = canvas_width - text_x - 10  # Right margin

            # Reposition and resize the text
            self.canvas.itemconfig(text_id, width=text_width)
            self.canvas.coords(text_id, (text_x, text_y))

            # Update 'last_bottom' for the next image-text pair
            # Add extra space after the text
            last_bottom = self.canvas.bbox(text_id)[3] + 70

            # Save the last bottom margin
            self.last_message_bottom = last_bottom
            

        # Update the 'scrollregion' to accommodate the new elements
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        

    def load_and_display_messages(self):
        # This method will load and display historical messages from the model
        messages = self.controller.model.get_messages()
        for message in messages:
            if message['role'] == 'user':
                self.display_message(message['content'], "user")
            elif message['role'] == 'assistant':
                self.display_message(message['content'], "bot")

    def create_round_image(self, img, size=(50, 50)):
        img = img.resize(size, Image.LANCZOS)
        mask = Image.new('L', img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)
        return img

    def load_config(self):
        # Load user image from configuration, or set to default if not available
        default_img = Image.open('user.png')
        rounded_image = self.create_round_image(default_img)
        self.user_image_raw = ImageTk.PhotoImage(rounded_image)

        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                user_image_data = config.get('user_image')
                if user_image_data:
                    user_image = Image.open(
                        BytesIO(base64.b64decode(user_image_data)))
                    rounded_image = self.create_round_image(user_image)
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
        self.geometry("1280x720")

        # Create a frame for the chat area
        self.chat_frame = tk.Frame(self, padx=30, pady=30)
        self.chat_frame.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Canvas for displaying messages
        self.canvas = tk.Canvas(
            self.chat_frame, bg='white', highlightthickness=0, relief='flat')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Scrollbar for the Canvas
        self.scrollbar = ttk.Scrollbar(
            self.chat_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        # Entry widget for user input
        self.entry_message = ttk.Entry(self)
        self.entry_message.grid(row=1, column=0, sticky='ew')
        self.entry_message.config(width=80)
        self.entry_message.focus()

        # Button to send message
        send_button = ttk.Button(self, text="Send", command=self.on_send)
        send_button.grid(row=1, column=1, sticky='ew')

        # Button to reset chat
        reset_button = ttk.Button(
            self, text="Reset Chat", command=self.on_reset_chat)
        reset_button.grid(row=1, column=4, sticky='ew')

        # Button to quit application
        quit_button = ttk.Button(self, text="Quit", command=self.on_quit)
        quit_button.grid(row=1, column=2, sticky='ew')

        # Button to change user photo
        change_image_button = ttk.Button(
            self, text="Change Photo", command=self.change_photo)
        change_image_button.grid(row=1, column=3, sticky='ew')

        # Bind the Enter key to the send button action
        self.entry_message.bind("<Return>", lambda event: send_button.invoke())
        self.canvas.bind('<Configure>', self.on_canvas_configure)

    def on_canvas_configure(self, event):
        # This method is called when the canvas is resized
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_send(self):
        user_input = self.entry_message.get()
        if user_input and not profanity.contains_profanity(user_input):
            # Muestra mensaje del usuario
            self.display_message(user_input, "user")
            self.controller.handle_user_input(
                user_input)  # Envía mensaje al controlador
            self.entry_message.delete(0, tk.END)
        elif profanity.contains_profanity(user_input):
            messagebox.showwarning(
                "Warning", "Please refrain from using inappropriate language.")
            self.entry_message.delete(0, tk.END)

    def on_reset_chat(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the chat history?"):
            self.controller.handle_reset_chat()

    def display_message(self, message, sender):
        if sender == "user":
            image_to_use = self.user_image
        else:
            image_to_use = self.bot_image

        # Display image
        image_id = self.canvas.create_image(
            5, self.last_message_bottom + 10, anchor='nw', image=image_to_use, tags=("image",))

        # Calculate position for text to align it with the image
        image_bbox = self.canvas.bbox(image_id)
        text_x = image_bbox[2] + 10  # X position right after the image
        # Y position aligned with the top of the image
        text_y = self.last_message_bottom + 15
        canvas_width = self.canvas.winfo_width()
        text_width = canvas_width - text_x - 10  # Margin on the right side

        # Display text
        text_id = self.canvas.create_text(text_x, text_y,
                                          anchor='nw', text=message, width=text_width, tags=("text",))

        # Update last message bottom position based on the size of the text
        text_bbox = self.canvas.bbox(text_id)
        padding_bottom = 70  # Padding below the text
        self.last_message_bottom = text_bbox[3] + padding_bottom

        

        # After adding new content, update the scrollregion so the scrollbar knows the new extent of the canvas.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Automatically scroll to the bottom so that the latest message is visible
        self.canvas.yview_moveto(1)

    def change_photo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.jpeg")])
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
