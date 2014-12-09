from flood_mapper.models.flood_status import FloodStatus

from django.conf import settings
from django import forms

from flood_mapper.models.village import Village

import decimal


class AddFlodStatusForm(forms.ModelForm):
    village = forms.ChoiceField(
        required=False,
        help_text="The village of the affected RT.")
    rw = forms.ChoiceField(
        required=False,
        help_text="The RW of the affected RT."
    )

    def __init__(self, *args, **kwargs):
        super(AddFlodStatusForm, self).__init__(*args, **kwargs)
        self.fields['rt'].choices = (('', '---------'),)
        self.fields['rw'].choices = (('', '---------'),)
        # TODO: only show the villages, that this user is allowed to sees
        self.fields['village'].choices = [('', '---------')] + [
            (village.id, village.name) for village in Village.objects.all()]

    def clean(self):
        cleaned_data = self.cleaned_data
        depth = cleaned_data.get('depth')
        if depth is not None:
            cleaned_data['depth'] = decimal.Decimal(depth)
        return cleaned_data

    class Meta:
        fields = ['village', 'rw', 'rt', 'depth', 'date_time', 'notes']
        model = FloodStatus
