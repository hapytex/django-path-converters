from django.urls import path, include
from django_path_converters.views import test_json, test_rest, link_group

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/<str:any>/', id),
    path('auth/reset/<path:ab>/', id),
    path('foo/<path:ab>/', id),
    path('foo/bar/', id),
    path('<user.username:user>/<auth.group:group>/', link_group),
]