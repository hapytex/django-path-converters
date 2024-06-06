from django.http import HttpResponse
from django.shortcuts import render

def link_article(request, article, user):
    article.author = user
    article.save()
    # print(user.username)
    return HttpResponse('linked')

def link_article_template(request, article, user):
    return render(request, 'paths/sample_form.html', {'article': article, 'user': user})