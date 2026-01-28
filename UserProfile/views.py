from django.shortcuts import render


from django.urls import reverse_lazy
from django.views.generic import CreateView

from UserProfile.forms import UserForm
from .models import User


# Create your views here.
class CreateUser(CreateView):
    model=User
    template_name='UserProfile/create_user.html'
    form_class=UserForm
    success_url=reverse_lazy("book-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs
    
    