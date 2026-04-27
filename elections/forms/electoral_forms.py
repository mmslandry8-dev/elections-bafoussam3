from django import forms
from elections.models import ElectoralList

class ElectoralListForm(forms.ModelForm):
    class Meta:
        model = ElectoralList
        fields = ["voter_id", "center", "station"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full p-2 mb-3 rounded text-black"
            })