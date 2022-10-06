import random
import json
import torch 
from model import NeuralNet
from nlutils import bag_of_word,tokenize
import pyttsx3
import requests
from bs4 import BeautifulSoup
import urllib.request 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r',encoding='utf8') as f:
    intents = json.load(f)

FILE = "data.pth"
data=torch.load(FILE)

input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


bot_name="MYBOT"

def getsomecont(lnk):
    # rq=requests.get(lnk)
    # soup=BeautifulSoup(rq.content,"html.parser")
    # val=str(soup.find('p'))
    # return val.partition(".")[0]
    try:
        html = urllib.request.urlopen(lnk)
    
        # parsing the html file
        htmlParse = BeautifulSoup(html, 'html.parser')
        return htmlParse.find_all("p")[1].get_text()
    except:
        return "visit here "+lnk+"\n"

def getresponse(msg):
    sentence = tokenize(msg)
    X=bag_of_word(sentence, all_words)
    X=X.reshape(1,X.shape[0])
    X=torch.from_numpy(X).to(device)

    output=model(X)
    _, predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item()>0.75:
        for intent in intents['intents']:
            if tag== intent["tag"]:
                return random.choice(intent['responses'])
    else:
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")
        res=""
        i=0
        for j in search(msg, tld="co.in",lang='en', num=5,start=1, stop=2, pause=2):
            other=""
            i=i+1
            if i==1:
                res=res+getsomecont(j)+"\n"
            else:
                other=other+j+"\n"
        return res+"link you can visit :-\n\n"+other

 
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty("voice", voice[1].id)
    engine.say(command)
    engine.runAndWait()

