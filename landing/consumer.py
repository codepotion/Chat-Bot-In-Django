from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from hugchat import hugchat
from hugchat.login import Login
import os

username = "rohansinghluckee@gmail.com"
password = "$cx6j-+ZHBSk.Re"


def ChatBotInstance(username, password):

    if os.path.exists(f"{username}.json"):
        cookie = f"{username}.json"
    else:
        sign = Login(username, password)
        cookies = sign.login()
        cookie_path_dir = "./"
        sign.saveCookiesToDir(cookie_path_dir)
        cookie = f"{username}.json"

    chatbot = hugchat.ChatBot(cookie_path=cookie)
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    return chatbot


# sleep(1)
# import asyncio
# await asyncio.sleep(1) intervals for output


# whatevere is being sent in text as self.send parameter it goes to the client
# whatever is getting printed in event['text'] known as event and consist the message from client


class CustSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.chatbot = ChatBotInstance(username, password)

        if self.chatbot:
            self.send({
                'type': 'websocket.accept'
            })
            print("connected")
        else:
            print('Not connected')

    def websocket_receive(self, event):
        chatbot = self.chatbot
        UserRequest = event['text']
        BotResponse = chatbot.chat(UserRequest)

        self.send({
            'type': 'websocket.send',
            'text': str(BotResponse)
        })

        print(f"Request : {UserRequest}")
        print(f"Response : {BotResponse}")

    def websocket_disconnect(self, event):
        print("connection closed", event)
        raise StopConsumer()


# class CustAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         await self.send({
#             'type': 'websocket.accept'
#         })
#         print("connection opened")

#     async def websocket_recieve(self, event):
#         await self.send({
#             'type': 'websocket.send',
#             'text': 'message recieved as ' + event['text']
#         })
#         print("message recieved : ", event['text'])

#     async def websocket_disconnect(self, event):
#         await self.send({
#             'type': 'websocket.disconnect',
#             'text': 'connection closed'
#         })
#         print("connection closed")
