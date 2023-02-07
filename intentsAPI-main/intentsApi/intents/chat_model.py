import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import requests
from spellchecker import SpellChecker
from langdetect import detect
#with open('intents.json') as json_data:
#    inte = json.load(json_data)
res=requests.get('http://127.0.0.1:8000/intentsWithoutID/')
inte = res.json()

data = pickle.load(open("./training_data", "rb"))
words = data['words']
labels = data['labels']
train_x = data['train_x']
train_y = data['train_y']

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')


def bag_of_words(s, words):
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]
    bag = [0 for _ in range(len(words))]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return (numpy.array(bag))


def predict_class(sentence):
    error_threshhold = 0.75
    # générer des probabilités à partir du modèle
    results = model.predict([bag_of_words(sentence, words)])[0]
    # filtrer les prédictions en dessous error_threshhold
    results = [[i, r] for i, r in enumerate(results) if r > error_threshhold]
    # trier par force de probabilité
    results.sort(key=lambda x: x[1], reverse=True)
    # tuple de retour d'intention et de probabilité
    return_list = []
    for r in results:
        return_list.append((labels[r[0]], r[1]))
    return return_list


def resp(inp):
    results = predict_class(inp)
    #si il ya un probabilite fort
    if results:
        while results:
            for i in inte:
                if i['tag'] == results[0][0]:
                    result = random.choice(i['responses'])
                    break
            break    
        return result
    else:
        #si il nya pas
        return ("please contact our support at email : ....")


def chatx():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        print(resp(inp))

def chat(inp):
    lang = detect(inp)
    if lang!="en":
        lang="fr"
    spell=SpellChecker(language=lang)
    inp = spell.correction(inp)
    results = predict_class(inp)
    if results:
        while results:
            for i in inte:
                if i['tag'] == results[0][0]:
                    result = random.choice(i['responses'])
                    break
            break    
        return result
    else:
        valo={'messages':inp}
        res=requests.post('http://127.0.0.1:8000/UnidentifiedMessages/',data =valo)
        return ("please contact our support at email : ....")
        

