from django.shortcuts import render

# Create your views here.
# search.views.py
from itertools import chain
from django.views.generic import ListView

from cases.models import CasesModel
from detection.models import CitizenProfile


class SearchView(ListView):
    template_name = 'searching/search_results.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            cases_results = CasesModel.objects.search(query)
            # citizen_profile_results = CitizenProfile.objects.search(query)

            if request.user.is_staff or request.user.is_superuser:
                queryset_chain = chain(
                    cases_results,
                    # citizen_profile_results
                )
                qs = sorted(queryset_chain,
                            key=lambda instance: instance.pk,
                            reverse=True)
                self.count = len(qs)  # since qs is actually a list
                return qs
            queryset_chain = chain(
                cases_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return CasesModel.objects.none()  # just an empty queryset as default
