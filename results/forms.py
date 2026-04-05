from django import forms
from .models import ResultBV

class ResultBVForm(forms.ModelForm):
    class Meta:
        model = ResultBV
        fields = ['bureau', 'total_voters', 'null_votes']

    def clean(self):
        cleaned_data = super().clean()

        total_voters = cleaned_data.get('total_voters')
        null_votes = cleaned_data.get('null_votes')

        if null_votes > total_voters:
            raise forms.ValidationError("Les bulletins nuls ne peuvent pas dépasser les votants")

        return cleaned_data