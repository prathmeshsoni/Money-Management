from django import forms

from .models import TypeModel


class TypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_name'].widget = forms.widgets.TextInput(
            attrs={
                'type': 'text', 'placeholder': 'Enter Type...',
                'class': 'form-control'
            }
        )

    class Meta:
        model = TypeModel
        fields = "__all__"
