from django import forms

from .models import AccountModel


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_name'].widget = forms.widgets.TextInput(
            attrs={
                'type': 'text', 'placeholder': 'Enter Account...',
                'class': 'form-control'
            }
        )

    class Meta:
        model = AccountModel
        exclude = [
            'user'
        ]
        fields = [
            'account_name',
        ]
