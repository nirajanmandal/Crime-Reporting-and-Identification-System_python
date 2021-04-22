from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'cases'

urlpatterns = [
    path('addcase/', AddCaseView.as_view(), name='add-case'),
    path('approvecase/<int:pk>', approve_view, name='approve-case'),
    path('listcases/', ListCaseView.as_view(), name='list-case'),
    path('wanted-list/', WantedCaseView.as_view(), name='wanted-list'),
    path('missing-list/', MissingCaseView.as_view(), name='missing-list'),
    path('found-list/', FoundCaseView.as_view(), name='found-list'),
    path('editcase/<int:pk>', UpdateCaseView.as_view(), name='edit-case'),
    path('deletecase/<pk>', delete_case, name='delete-case'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
