from django.urls import path, include
from django_path_converters.views import link_article, link_article_template
from django.contrib import admin
from django.views.generic import TemplateView

def null_view(request, *args, **kwargs):
    return HttpResponse('nothing to see here')

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/<str:any>/', null_view),
    path('auth/reset/<path:ab>/', null_view),
    path('foo/<path:ab>/', null_view),
    path('foo/bar/', null_view),
    path('<article:article>/<user.username:user>/link/', link_article_template),
    path('<article:article>/<user.id:user>/link-them/', link_article, name='link-article'),
    path('<path:wildcard>', null_view),
    path('unreachable', null_view),
]