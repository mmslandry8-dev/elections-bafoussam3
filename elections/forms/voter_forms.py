from django import forms

class VoterLookupForm(forms.Form):
    voter_id = forms.CharField(max_length=100)