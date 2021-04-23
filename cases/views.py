import csv

from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CaseForm, CasesModel

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class AddCaseView(CreateView):
    template_name = 'cases/add_cases.html'
    form_class = CaseForm
    success_url = reverse_lazy('accounts:dashboard')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login first')
            return redirect('accounts:login')
        else:
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # instance = form.save(commit=False)
            form.save()
            messages.success(request, 'Case added successfully')
            return redirect('accounts:dashboard')

        # messages.error(request, 'Please check your credentials again')
        return render(request, self.template_name, {'form': form})


@login_required
def download_case(request, pk):
    try:
        case = CasesModel.objects.get(pk=pk)
    except CasesModel.DoesNotExist:
        messages.error(request, "Case not found")
        return redirect('cases:list-case')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Details.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'address', 'nationality', 'contact_number', 'email',
                     'gender', 'date_of_case', 'status', 'description'])

    writer.writerow([case.first_name, case.last_name, case.address, case.contact_number,
                     case.nationality, case.description,
                     case.image, case.status])
    return response


@login_required
def approve_view(request, pk):
    approve = CasesModel.objects.get(pk=pk)
    approve.is_approved = not approve.is_approved
    approve.save()
    return redirect('cases:list-case')


@method_decorator(login_required, name='dispatch')
class ListCaseView(ListView):
    template_name = 'cases/list_cases.html'
    model = CasesModel
    context_object_name = 'cases'
    paginate_by = 4


@method_decorator(login_required, name='dispatch')
class WantedCaseView(ListView):
    template_name = 'cases/list-wanted.html'
    model = CasesModel
    context_object_name = 'cases'


@method_decorator(login_required, name='dispatch')
class MissingCaseView(ListView):
    template_name = 'cases/list-missing.html'
    model = CasesModel
    context_object_name = 'cases'


@method_decorator(login_required, name='dispatch')
class FoundCaseView(ListView):
    template_name = 'cases/list-found.html'
    model = CasesModel
    context_object_name = 'cases'


@login_required
def delete_case(request, pk):
    try:
        case = CasesModel.objects.get(pk=pk)
    except CasesModel.DoesNotExist:
        messages.error(request, "Case not found")
        return redirect('cases:list-case')
    case.delete()
    messages.success(request, "Case deleted successfully")
    return redirect('cases:list-case')


@method_decorator(login_required, name='dispatch')
class UpdateCaseView(UpdateView):
    model = CasesModel
    form_class = CaseForm
    template_name = 'cases/update_cases.html'
    context_object_name = 'case'

    def form_valid(self, form):
        case = form.save(commit=False)
        case.updated_by = self.request.user
        case.updated_at = timezone.now()
        case.save()
        return redirect('cases:list-case')






