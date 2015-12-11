from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from portal.forms import QuestionForm
from portal.Constants import *
import requests
import nltk
import json
from nltk.stem.wordnet import WordNetLemmatizer
from review_model_helper.models import ProductReviews, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from portal.paraSumm import summarize


def get_product_reviews(product_id):
    reviews = ProductReviews.objects.filter(product_id=product_id)
    document = ''.join([review.review_text for review in reviews])
    print(document)
    return document


def req_rank_retrieve(qn, product_id):
    params['text'] = qn
    r = requests.get(ALCHEMY_URL, params=params)
    data = r.json()
    keyWords=[]
    try:
        for dt in data['keywords']:
            keyWords.append(dt['text'])
    except KeyError:
        print("KeyError")
    print("keywords, ", keyWords)
    lemmatizer = WordNetLemmatizer()
    document = get_product_reviews(product_id)
    sentences = nltk.sent_tokenize(document)
    document = []
    for sent in sentences:
        sent_list = []
        for word in nltk.word_tokenize(sent):
            sent_list.append(word)
        document.append(sent_list)
    answers = []
    and_sent = set()
    for sent_i in range(0, len(document)):
        sent = document[sent_i]
        sent_lemma = []
        for st in sent:
            sent_lemma.append(lemmatizer.lemmatize(st))
        for keyword in keyWords:
            if lemmatizer.lemmatize(keyword) in sent_lemma:
                and_sent.add(sent_i)
    for s_id in and_sent:
        answers.append(' '.join(document[s_id]))
    print(answers)
    answers = ''.join(answers)
    return ''.join(summarize(answers))


def product_view(request, product_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            qn = form.cleaned_data['question']
            answers = req_rank_retrieve(qn, product_id)
            return render(request, 'portal/answer.html', {'answers': answers})
    else:
        form = QuestionForm()

    return render(request, 'portal/product.html', {'form': form, 'product_id':product_id})


def index_view(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'portal/index.html', {"products": products})