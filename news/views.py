from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from detection.models import CitizenProfile
from django.views.generic import ListView, DetailView


@method_decorator(login_required, name='dispatch')
class NewsView(ListView):
    template_name = 'news/news.html'
    model = CitizenProfile
    context_object_name = 'news'
