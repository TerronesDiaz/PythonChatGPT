This repository contains a Python-based chatbot powered by OpenAI. The chatbot can have interactive conversations with users on various     
topics. You can choose the model you want from those currently available.

## Installation

To install and use the OpenAI Chatbot, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/TerronesDiaz/PythonChatGPT.git
   ```

2. Navigate to the project directory:
   ```bash
   cd PythonChatGPT
   ```

3. Install the required dependencies using pip:

   if you dont have pip installed:
   python -m pip install --upgrade pip


The following dependencies are required:
- better_profanity (install with `pip install better_profanity`)
- Pillow (install with `pip install Pillow`)
- OpenAI (install with `pip install openai`)
- typer (install with `pip install typer`)
- rich (install with `pip install rich`)
- python-dotenv (optional, install with `pip install python-dotenv`)


4. Set up your OpenAI API key in a `.env` file:
   ```bash
   echo "api_key=YOUR_API_KEY" > .env
   ```

5. Start the chatbot:
   ```bash
   python chat_controller.py
   ```

## Usage

The OpenAI Chatbot provides a conversational interface where users can interact with the chatbot on various topics. The chatbot supports commands such as 
`exit`, `new`, and `help` to manage the conversation.

## Features:

- `Profile picture:`: You can customize the profile picture when you send a message.
- `Reset Chat`: You can reset the conversation at any time with the reset chat button
- `Save your conversation`: The bot will not forget the information you have provided unless you reset the conversation.

## Contributing

If you would like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
