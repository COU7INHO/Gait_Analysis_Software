import sys

import openai
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

# Set your OpenAI API key
openai.api_key = "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"


class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        text_output_label = QLabel("Output:")
        self.text_output = QTextBrowser(self)
        self.text_output.setReadOnly(True)

        text_input_label = QLabel("Ask something:")
        self.text_input = QLineEdit(self)
        input_button = QPushButton("->")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(input_button)

        main_layout.addWidget(text_output_label)
        main_layout.addWidget(self.text_output)
        main_layout.addWidget(text_input_label)
        main_layout.addLayout(input_layout)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Connect the text input to the chat function
        input_button.clicked.connect(self.chat_with_bot)

        # Set window properties
        self.setWindowTitle("Chat with GPT-3")
        self.setGeometry(100, 100, 600, 400)

    def chat_with_bot(self):
        # Get the user's input and send it to the OpenAI model
        user_input = self.text_input.text()
        response = chat(user_input)

        # Append the user's input and the bot's response to the text output
        self.text_output.append(f"You: {user_input} \n")
        self.text_output.append(f"Bot: {response}")

        # Clear the input field
        self.text_input.clear()


def chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotApp()
    window.show()
    sys.exit(app.exec_())
