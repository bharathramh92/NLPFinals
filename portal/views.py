from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from portal.forms import QuestionForm
from portal.Constants import *
import requests
import nltk
import json
from nltk.stem.wordnet import WordNetLemmatizer
from review_model_helper.models import ProductReviews, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from portal.paraSumm import summarize
import re
from django.core.exceptions import ObjectDoesNotExist


def get_product_reviews(product_id):
    reviews = ProductReviews.objects.filter(product_id=product_id)
    document = ''.join([review.review_text for review in reviews])
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
    if len(keyWords) == 0:
        # if there are no keywords in a question, this function can terminate.
        return None
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
    and_sent = set()    # to store sentence index whose keywords were matched.
    for sent_i in range(0, len(document)):
        sent = document[sent_i]
        # lemmatization check as well.
        sent_lemma = []
        for st in sent:
            sent_lemma.append(lemmatizer.lemmatize(st))
        for keyword in keyWords:
            if lemmatizer.lemmatize(keyword) in sent_lemma:
                and_sent.add(sent_i)
    for s_id in and_sent:
        answers.append(' '.join(document[s_id]))
    # print(answers)
    answers = ''.join(answers)
    summarized_answer = ''.join(summarize(answers))
    summarized_answer = re.sub('[^a-zA-Z0-9\s\.]', '', summarized_answer)
    print("summarized answer ", summarized_answer)
    if len(summarized_answer) == 0:
        return None
    return summarized_answer


def product_view(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            qn = form.cleaned_data['question']
            answers = req_rank_retrieve(qn, product_id)
            return render(request, 'portal/answer.html', {'answers': answers, 'product_id': product_id, 'qn': qn})
    else:
        form = QuestionForm()

    return render(request, 'portal/product.html', {'form': form, 'product_id': product_id, 'product': product})


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