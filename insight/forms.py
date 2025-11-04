from django import forms


class DateFiltersForm(forms.Form):
    start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
