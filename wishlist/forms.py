from django import forms
from .models import Wishlist


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].widget.attrs['readonly'] = True
        placeholders = {
            'name': 'List Name',
            'description': 'List Description'
        }

        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 enquiry-form-input'
            self.fields[field].label = False