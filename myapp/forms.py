from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["user"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email (optional)"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter address",
                "rows": 3
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make image required in the form
        self.fields["image"].required = True
        self.fields["image"].error_messages = {
            "required": "Please upload a contact image."
        }