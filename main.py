from hugchat import hugchat
import os
import json


class Login:
    def init(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.cookies = None
        self.chatbot = None  # Initialize chatbot to None

    def login(self):
        # Replace this with your actual login implementation
        cookies = {"example_cookie": "cookie_value"}
        self.cookies = cookies
        return cookies

    def save_cookies(self):
        if not os.path.exists("usercookies"):
            os.makedirs("usercookies")
        with open(f"usercookies/{self.email}.json", "w") as f:
            json.dump(self.cookies, f)

    def load_cookies(self):
        with open(f"usercookies/{self.email}.json", "r") as f:
            cookies = json.load(f)
        return cookies

    def create_chatbot(self):
        if self.chatbot is None:
            self.chatbot = hugchat.ChatBot(cookies=self.cookies)


def start_chat(email, passwd, searchinput):
    sign = Login(email, passwd)

    # Check if cookies and chatbot are already present
    if sign.cookies is None or sign.chatbot is None:
        cookies = sign.login()
        sign.save_cookies()

        # Create the chatbot if it doesn't exist
        sign.create_chatbot()
    else:
        cookies = sign.cookies

    conversation_id = sign.chatbot.new_conversation()
    sign.chatbot.change_conversation(conversation_id)

    # Adjust the parameters to potentially reduce response times
    response = sign.chatbot.chat(
        searchinput,
        temperature=0.2,
        max_new_tokens=1024,  # Experiment with a lower value
        top_k=10,  # Experiment with lower values
        top_p=0.7,  # Experiment with lower values
        use_cache=True  # Enable response caching
    )
    print(response)
    # Ensure response is 2 to 3 sentences
    sentences = response.split('.')
    response = '. '.join(sentences[:3])

    # Ensure response ends with a full stop
    if not response.endswith('.'):
        response += '.'

    return response


def start_chat_with_bot(email, passwd, input_text):
    chat_response = start_chat(email, passwd, input_text)
    return chat_response
