from openai import OpenAI
# Configuration file to call api_key from the .env
from config.config import api_key
import typer
from rich import print
from rich.table import Table
import sys

def main():
    """Main function to run the OpenAI Chatbot."""
    
    # Create a client with your own API key
    client = OpenAI(api_key=api_key)
    print("[bold green]Welcome to the OpenAI Chatbot![/bold green]")
    context = {"role": "system",
                "content": "I am a helpful assistant created by OpenAI. How can I help you today?"}
    messages = [context]
    while True:
        content, messages = prompt_user(messages)

        print(f"[bold purple]You:[/bold purple] {content}")
        if content.lower() == "exit":
            print("Are you sure you want to exit the chatbot? (y/n) or (yes/no)")
            exit_response = input().strip().lower()
            if exit_response == "yes" or exit_response == "y":
                print("👋 Goodbye! 👋")
                sys.exit(0)
            elif exit_response == "no" or exit_response == "n":
                print("Let's Continue the conversation then! 😄 ")
                continue
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue
        elif content.lower() == "help":
            show_help()
            continue

        try:
            response, messages = get_response(client, content, messages)
            print(f'[bold green]ChatBot: [/bold green] {response}')
        except Exception as e:
            print(f"[bold red]Error:[/bold red] Failed to get a response from OpenAI: {str(e)}")

def get_response(client, content, messages):
    """Get a response from the OpenAI API based on the user's input."""

    messages.append({"role": "user", "content": content})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    response_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": response_message})
    return response_message, messages

def prompt_user(messages):
    """Prompt the user for input and handle special commands."""

    while True:
        prompt_text = "\nWhat do you want to ask or to talk about? "
        user_input = input(prompt_text).strip()
        if not user_input:
            print("Please enter a non-empty input.")
        elif user_input.lower() == "new":
            print("🔄 Starting a new conversation 🔄 \n")
            messages = [{"role": "system", "content": "I am a helpful assistant created by OpenAI. How can I help you today?"}]
            continue
        else:
            return user_input, messages

def show_help():
    """Display help information for the chatbot."""

    table = Table("Commands", "Description")
    table.add_row("exit", "Exit the chatbot")
    table.add_row("new", "Start a new conversation (clears the chat history)")
    table.add_row("help", "Show this help message again")
    print(table)

if __name__ == "__main__":
    typer.run(main)
