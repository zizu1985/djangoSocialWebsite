from django.conf.urls import url
from . import views

# images/create -> views.image_create
urlpatterns = [
    url(r'^create/$', views.image_create, name='create'),
]

