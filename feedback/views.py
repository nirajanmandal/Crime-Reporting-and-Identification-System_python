from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from cases.models import CasesModel
from feedback.forms import FeedbackForm
from .models import FeedbackModel


class FeedbackView(CreateView):
    template_name = 'feedback/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('accounts:dashboard')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login first')
            return redirect('accounts:login')
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(kwargs)
        context_data['feedback_count'] = FeedbackModel.objects.all().count()
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            case_pk = kwargs.get('case_pk')
            case = CasesModel.objects.get(id=case_pk)
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.case = case
            obj.save()
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            attachment = form.cleaned_data['image']
            message = form.cleaned_data['message']

            email = EmailMessage(subject, message, from_email, ['carljhonsonsa500@gmail.com'])
            try:
                email.attach(attachment.name, attachment.content_type)
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Feedback sent successfully')
            return redirect('feedback:feedback', case_pk)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class FeedbackInfo(ListView):
    template_name = 'feedback/feedback-info.html'
    model = FeedbackModel
    context_object_name = 'feedback_info'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['feedback_count'] = FeedbackModel.objects.all().count()
        return context_data
