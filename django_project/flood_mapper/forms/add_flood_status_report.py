from flood_mapper.models.flood_status import FloodStatus

from django.conf import settings
from django import forms

from flood_mapper.models.village import Village
from flood_mapper.models.rw import RW
from flood_mapper.models.rt import RT

import decimal


class AddFlodStatusForm(forms.ModelForm):
    village = forms.ChoiceField(
        required=False,
        help_text="The village of the affected RT."
    )
    rw = forms.ChoiceField(
        required=False,
        help_text="The RW of the affected RT.",
        choices=[
            (rw_choice.id, rw_choice.name) for rw_choice in RW.objects.all()
        ]
    )

    def __init__(self, *args, **kwargs):
        super(AddFlodStatusForm, self).__init__(*args, **kwargs)
        self.fields['rt'].widget.choices = [('', '---------')]
        self.fields['rw'].widget.choices = [('', '---------')]
        print self.fields['rw'].validators
        # TODO: only show the villages, that this user is allowed to sees
        self.fields['village'].choices = [('', '---------')] + [
            (village.id, village.name) for village in
            Village.objects.order_by('name')]

    def clean(self):
        cleaned_data = self.cleaned_data
        depth = cleaned_data.get('depth')
        if depth is not None:
            cleaned_data['depth'] = decimal.Decimal(depth)
        print cleaned_data
        print self.errors
        return cleaned_data

    class Meta:
        fields = ['village', 'rw', 'rt', 'depth', 'date_time', 'notes']
        model = FloodStatus
