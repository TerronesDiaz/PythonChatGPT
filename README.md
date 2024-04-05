This repository contains a Python-based chatbot powered by OpenAI's GPT-3 model. The chatbot can have interactive conversations with users on various     
topics.

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
   - OpenAI (install with `pip install openai`)
   - typer (install with `pip install typer`)
   - rich (install with `pip install rich`)
   - dotenv (install with `pip install python-dotenv`)

4. Set up your OpenAI API key in a `.env` file:
   ```bash
   echo "api_key=YOUR_API_KEY" > .env
   ```

5. Start the chatbot:
   ```bash
   python main.py
   ```

## Usage

The OpenAI Chatbot provides a conversational interface where users can interact with the chatbot on various topics. The chatbot supports commands such as 
`exit`, `new`, and `help` to manage the conversation.

## Commands

- `exit`: Exit the chatbot
- `new`: Start a new conversation (clears the chat history)
- `help`: Show help message

## Contributing

If you would like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
