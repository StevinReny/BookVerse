from django import forms
from django.db import models

from books.models import Books

class BookForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'