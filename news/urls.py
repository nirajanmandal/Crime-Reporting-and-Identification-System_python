from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'news'
urlpatterns = [
    path('news/', NewsView.as_view(), name='list-news'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
