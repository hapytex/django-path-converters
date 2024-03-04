from django.urls import path
from django_path_converters.views import test_json, test_rest, link_group

urlpatterns = [
    path('<user.username:user>/<auth.group:group>/', link_group),
    path('<unsafejson:item>/', test_json),
    path('<path:rest>/', test_rest),
]