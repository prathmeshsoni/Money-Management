from django import forms

from .models import ManageModel


class ManageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].required = False
        self.fields['category'].required = False
        self.fields['to_account'].required = False
        self.fields['from_account'].required = False
        self.fields['note'].required = False
        self.fields['date_name'].widget = forms.widgets.TimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control datetimepicker',
            },
        )
        self.fields['note'].widget = forms.Textarea(
            attrs={
                'cols': '30',
                'rows': '5',
                'placeholder': 'Enter Note...'
            },
        )
        self.fields['amount'].widget = forms.NumberInput(attrs={'placeholder': 'Enter Amount...'})

    class Meta:
        model = ManageModel

        exclude = [
            'user'
        ]
        fields = [
            'type',
            'date_name',
            'account',
            'category',
            'amount',
            'note',
            'to_account',
            'from_account',
        ]
