from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput
from .models import User  # assuming your custom user model

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "first_name", "last_name", "contact_number" ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = user

    #     if user and not user.is_superuser:
    #         self.fields['role'].choices = [('customer', "Customer")]
    #         self.fields['role'].widget = HiddenInput()
    #     else:
    #         self.fields['role'].choices = [('admin', "Admin")]
    #         self.fields['role'].widget = HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=False)

        # Set role based on who is creating the user
        if self.current_user and self.current_user.is_superuser:
            user.role = 'admin'
        else:
            user.role = 'customer'

        if commit:
            user.full_clean()
            user.save()
        return user
