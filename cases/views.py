from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

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


# @method_decorator(login_required, name='dispatch')
# class DeleteCaseView(DeleteView):
#     model = CasesModel
#     template_name = 'cases/cases_confirm_delete.html'
#     success_url = reverse_lazy('cases:list-case')


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
    success_url = reverse_lazy('cases:list-case')
    context_object_name = 'case'

    def post(self, request, *args, **kwargs):
        try:
            case = self.get_object()
        except CasesModel.DoesNotExist:
            case = None
        case_form = CaseForm(self.request.POST or None, self.request.FILES or None, instance=case)

        if case_form.is_valid():
            with transaction.atomic():
                cas = case_form.save(commit=False)
                cas.save()
                messages.success(request, 'Profile was successfully updated')
                return redirect('accounts:dashboard')
        print(case_form.errors)
        messages.warning(request, 'Please check your credentials')




