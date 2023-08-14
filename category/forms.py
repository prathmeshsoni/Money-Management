from django import forms

from .models import CategoryModel


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat_name'].widget = forms.widgets.TextInput(
            attrs={
                'type': 'text', 'placeholder': 'Enter Category...',
                'class': 'form-control'
            }
        )

    class Meta:
        model = CategoryModel
        exclude = [
            'user'
        ]
        fields = [
            'cat_name',
        ]
