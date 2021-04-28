from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'feedback'
urlpatterns = [
    path('feedback/<int:case_pk>', FeedbackView.as_view(), name='feedback'),
    path('feedback-info/', FeedbackInfo.as_view(), name='feedback-info'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
