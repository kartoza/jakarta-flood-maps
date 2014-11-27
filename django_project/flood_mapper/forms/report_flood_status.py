from flood_mapper.models.flood_status import FloodStatus

from django.conf import settings
from django import forms


class EnquiryForm(forms.ModelForm):
    village = forms.CharField(required=False)
    rw = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.rw.choices = (('rw', 'rw'))
        self.village.choices = (('village', 'village'))
        super(EnquiryForm, self).__init__(*args, **kwargs)


    class Meta:
        model = FloodStatus
