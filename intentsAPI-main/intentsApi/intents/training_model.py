from gettext import install
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy
import tflearn
import tensorflow
import random
import pickle
import json, requests, pprint
#with open('Intents.json') as json_data:
#    data = json.load(json_data)
def chat():
    
    resp = requests.get('http://127.0.0.1:8000/intentsWithoutID/')
    data = resp.json()


    words = []
    labels = []
    docs_x = []
    docs_y = []
    ignore_words = ['?','you','the', 'a', 'an','do','what','where','why','to','from','if','which' ]
    for intent in data:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [lemmatizer.lemmatize(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    tensorflow.compat.v1.reset_default_graph()


    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save('./intents/model.tflearn')

    pickle.dump( {'words':words, 'labels':labels, 'train_x':training, 'train_y':output}, open( "./intents/training_data", "wb" ) )
    print("fin")
