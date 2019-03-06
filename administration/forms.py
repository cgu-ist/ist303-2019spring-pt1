from django import forms


class ServiceForm(forms.Form):
    name = forms.CharField()
    slug = forms.SlugField()
    minutes = forms.CharField()
    rate = forms.DecimalField
