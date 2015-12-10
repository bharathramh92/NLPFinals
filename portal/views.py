from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from portal.forms import QuestionForm
from portal.Constants import *
import requests
import nltk
import json


def ie_preprocess(keyWords):
    with open("sample_review_baby.json") as fl:
        data = json.loads(fl.read())
        document = ''.join([dt["reviewText"] for dt in data])
        # print(document)
        sentences = nltk.sent_tokenize(document)
        # print(sentences)
        document = [nltk.word_tokenize(sent) for sent in sentences]
        print(document)
        for sent in document:
            for keyword in keyWords:
                if keyword in sent:
                    print(sent)
        return keyWords


def req_rank_retrieve(qn):
    params['text'] = qn
    r = requests.get(ALCHEMY_URL, params=params)
    data = r.json()
    keyWords=[]
    try:
        for dt in data['keywords']:
            keyWords.append(dt['text'])
    except KeyError:
        print("KeyError")
    print(keyWords)
    return ie_preprocess(keyWords)


def index_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            qn = form.cleaned_data['question']
            answers = req_rank_retrieve(qn)
            return render(request, 'portal/answer.html', {'answers': answers})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QuestionForm()

    return render(request, 'portal/index.html', {'form': form})