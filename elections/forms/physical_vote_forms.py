from django import forms
from elections.models import PollingStation, Party


class PhysicalResultForm(forms.Form):

    station = forms.ModelChoiceField(
        queryset=PollingStation.objects.none(),  # 🔥 VIDE AU DÉPART
        label="Bureau de vote",
        widget=forms.Select(attrs={
            "class": "w-full p-2 mb-4 rounded text-black"
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 FILTRAGE PAR CENTRE
        if user and user.role == "AGENT" and user.center:
            self.fields["station"].queryset = PollingStation.objects.filter(
                center=user.center
            )
        else:
            # fallback admin
            self.fields["station"].queryset = PollingStation.objects.all()

        # 🔥 CHAMPS PARTIS
        for party in Party.objects.all():
            self.fields[f"party_{party.id}"] = forms.IntegerField(
                label=party.name,
                min_value=0,
                required=False,
                widget=forms.NumberInput(attrs={
                    "class": "w-full p-2 mb-3 rounded text-black"
                })
            )