from django.shortcuts import render, HttpResponse
from django.conf import settings
from hugchat import hugchat
from hugchat.login import Login
import json
import os


# Create your views here.
husername = settings.HUSERNAME
hsecret = settings.HSECRETKEY


def ChatBotCreateCookie(husername=husername, hsecret=hsecret):
    sign = Login(husername, hsecret)
    cookies = sign.login()
    cookie_path_dir = "./"
    sign.saveCookiesToDir(cookie_path_dir)
    return cookies


def ChatBotVerifyCookie(husername=husername):
    if os.path.exists(f"{husername}.json"):
        cookie = f"{husername}.json"
    else:
        ChatBotCreateCookie()
        cookie = f"{husername}.json"
    return cookie


def ChatBotLogin(request):
    cookie = ChatBotVerifyCookie()
    chatbot = hugchat.ChatBot(cookie_path=cookie)
    chat_id = chatbot.new_conversation()
    chatbot.change_conversation(chat_id)
    return chatbot


def LandingFunction(request):
    return render(request, 'index.html')


def ChattingRequest(request):

    with open('training.txt', 'r') as f:
        data = f.read()

    prefix = str(data) + '''
                            use above data if required, 
                            treat it as chat history (user for user and bot for your response),
                            generate responses like you have interacted with the user before,
                            dont greet everytime,
                            dont add Bot before your response
                         '''

    ChatRequestString = request.GET['ReqText']
    ChatRequest = prefix+ChatRequestString

    ChatConn = ChatBotLogin(request)
    ChatResponse = ChatConn.chat(ChatRequest)

    AppendData = "\nuser="+str(ChatRequestString)+".\nbot="+str(ChatResponse)
    with open('training.txt', 'a') as f:
        f.write(AppendData)

    return HttpResponse(str(ChatResponse))
