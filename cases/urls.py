from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'cases'

urlpatterns = [
    path('addwanted/', AddCaseView.as_view(), name='add-case'),
    path('listwanted/', ListCaseView.as_view(), name='list-case'),
    path('editwanted/<int:pk>', UpdateCaseView.as_view(), name='edit-case'),
    path('deletewanted/<pk>', delete_case, name='delete-case'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
