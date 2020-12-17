from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'cases'

urlpatterns = [
    path('addwanted/', AddCaseView.as_view(), name='add-case'),
    path('listcases/', ListCaseView.as_view(), name='list-case'),
    path('wanted-list/', WantedCaseView.as_view(), name='wanted-list'),
    path('missing-list/', MissingCaseView.as_view(), name='missing-list'),
    path('editwanted/<int:pk>', UpdateCaseView.as_view(), name='edit-case'),
    path('deletewanted/<pk>', delete_case, name='delete-case'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
