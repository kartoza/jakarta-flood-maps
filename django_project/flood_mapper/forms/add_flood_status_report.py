# -*- coding: utf-8 -*-
"""**Forms used to add new flood status reports**

.. tip::
   The AddFloodStatusReport form class is essentially a model form with the
   addition of related fields village and rw.

"""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '08/12/2014'
__license__ = "GPL"

from django import forms

import decimal
from datetime import datetime

from flood_mapper.models.village import Village
from flood_mapper.models.rw import RW
from flood_mapper.models.rt import RT
from flood_mapper.models.flood_status import FloodStatus


class AddFloodStatusForm(forms.ModelForm):
    """This form is used to capture details of a newly entered flood.
    """
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
        super(AddFloodStatusForm, self).__init__(*args, **kwargs)
        if args:
            village_id = args[0].get('village')
            rw_id = args[0].get('rw')
        else:
            village_id = None
            rw_id = None
        # TODO: only show the villages, that this user is allowed to see
        self.fields['village'].choices = [('', '---------')] + [
            (village.id, village.name) for village in
            Village.objects.order_by('name')
        ]
        if village_id:
            self.fields['rw'].widget.choices = [('', '---------')] + [
                (rw.id, rw.name) for rw in
                RW.objects.filter(village__id=village_id).order_by('name')
            ]
        else:
            self.fields['rw'].widget.choices = [('', '---------')]
        if rw_id:
            self.fields['rt'].widget.choices = [('', '---------')] + [
                (rt.id, rt.name) for rt in
                RT.objects.filter(rw__id=rw_id).order_by('name')
            ]
        else:
            self.fields['rt'].widget.choices = [('', '---------')]
        self.fields['date_time'].initial = datetime.now()

    def clean(self):
        cleaned_data = self.cleaned_data
        depth = cleaned_data.get('depth')
        if depth is not None:
            cleaned_data['depth'] = decimal.Decimal(depth)
        return cleaned_data

    class Meta:
        fields = ['village', 'rw', 'rt', 'depth', 'date_time', 'notes']
        model = FloodStatus
