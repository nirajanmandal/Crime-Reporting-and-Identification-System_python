from django.urls import path
from .views import SearchView

app_name = 'searching'
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),

]
