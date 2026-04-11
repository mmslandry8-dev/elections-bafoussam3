from django import forms
from elections.models import VoteSession

class VoteSessionForm(forms.ModelForm):

    class Meta:
        model = VoteSession
        fields = ["polling_station", "total_voters", "blank_votes"]
    
    # class Meta:
    #     model = VoteSession
    #     fields = ["Bureau_de_vote", "Nombre_totals_de_votants ", "Bulletins_nuls"]