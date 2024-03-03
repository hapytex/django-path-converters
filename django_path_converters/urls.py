from django.urls import path, include

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/<str:any>/', id),
    path('auth/reset/<path:ab>/', id),
    path('foo/<path:ab>/', id),
    path('foo/bar/', id),
]