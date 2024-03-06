from django.http import HttpResponse

def link_group(request, user, group):
    return HttpResponse('link')

def test_json(request, item):
    print(item, type(item))
    return HttpResponse(str(('json', item, type(item))))

def test_rest(request, rest):
    print(rest, type(rest))
    return HttpResponse(str(('rest', rest, type(rest))))