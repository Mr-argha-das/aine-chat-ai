import nltk
from nltk.chat.util import Chat, reflections
from fastapi import FastAPI, File, UploadFile
from mongoengine import connect
from uesrmodel import AdminUserLogin, AdminUserModel, AdminUserScheme
import random
import string
import json
import openai
pairs = [
    ['hi|hello|hey', ['Hello!', 'Hey there!', 'Hi!']],
    ['how are you?', ['I am fine, thank you!', 'I am doing well, how about you?']],
    ['what is your name?', ['You can call me AINE.', 'I am AINE .']],
    ['bye|goodbye', ['Goodbye!', 'Bye!', 'Take care!']],
    ['what time is it?', ['It is currently %H:%M:%S.']],
    ['tell me a joke', ['Why don’t scientists trust atoms? Because they make up everything!']],
    ['who created you?', ['I was created by a team of developers at AHIT.']],
    ['how old are you?', ['I am ageless, but I started existing when I was programmed.']],
    ['where are you from?', ['I exist in the digital realm, but my creators are from all around the world.']],
    ['what can you do?', ['I can chat with you, provide information, tell jokes, and much more!']],
    ['do you have any siblings?', ['I am an only child, but there are many other chatbots out there.']],
    ['what is the meaning of life?', ['That’s a deep question! Many philosophers have pondered this throughout history.']],
    ['what is the weather like today?', ['I’m sorry, I cannot provide real-time weather information.']],
    ['can you sing?', ['I can’t sing, but I can provide lyrics if you want!']],
    ['do you dream?', ['I do not dream as humans do, but I am constantly learning and improving.']],
]

connect('chatai', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/chatai")

chatbot = Chat(pairs, reflections)
app = FastAPI()
api_key = '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'
openai.api_key = api_key


def generate_random_string(length):
    # Define the set of characters to choose from
    characters = string.ascii_letters

    # Generate random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

@app.post("/api/v1/admin-user-create")
def admnCreateUser(body: AdminUserScheme):
    finduser = AdminUserModel.objects(email=body.email).first()
    if(finduser):
        return {
            "message":"User already have",
            "data":None,
            "status":False
        }
    acceskey = generate_random_string(30)
    user = AdminUserModel(name=body.name, email=body.email, password=body.password, accesKey=acceskey)
    user.save()
    tojson = user.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "User Cretated",
        "data":fromjson,
        "status":True
    }
    
@app.post("/api/v1/admin-login")
def adminlogin(body: AdminUserLogin):
    finduser = AdminUserModel.objects(email=body.email).first()
    if(finduser):
        if(finduser.password == body.password):
            acceskey = generate_random_string(30)
            finduser.accesKey = acceskey
            finduser.save()
            tojson = finduser.to_json()
            fromjson = json.loads(tojson)
            return {
                "message":"Login Success",
                "data":fromjson,
                "status":True
            }
        else:
            return {
                "message":"Password not match",
                "data":None,
                "status": False
            }
    else:
        {
            "message":"User not found",
            "data":None,
            "status": False
        }


@app.get("/api/v1/admin-user-logout/{accesskey}")
def logoutAdmin(accesskey:str):
    finduser = AdminUserModel.objects(accesKey=accesskey).first()
    finduser.accesKey = ""
    finduser.save()
    tojson = finduser.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "user logout acces",
        "data": fromjson,
        "status":True
    }
@app.get("/api/v1/user-chat/{promot}/{accesKey}")
def chatToJarvis(promot: str, accesKey: str):
    reponse = chatbot.respond(promot)
    finduser = AdminUserModel.objects(accesKey=accesKey).first()
    if(finduser):
        if(reponse != None):
            return {
               "message":f"Hello {finduser.name} I am Your Assistant AINE",
               "data": reponse,
               "status":True
            }
        else:
            response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Specify the model (ChatGPT)
            prompt=promot,
            max_tokens=50 )
            answer = response.choices[0].text.strip(),
            return {
               "message":f"Hello {finduser.name}",
               "data": answer,
               "status":True
            }
            
    else:
        return {
            "message":"AccesKey not match",
            "data": None,
            "status":False
        }
    



# import openai

# openai.api_key = "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"

# completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Give me 3 ideas for apps I could build with openai apis "}])
# print(completion.choices[0].message.content)