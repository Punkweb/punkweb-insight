from django import forms


class IndexFiltersForm(forms.Form):
    start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "pw-input", "type": "date"}),
    )
    end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "pw-input", "type": "date"}),
    )
