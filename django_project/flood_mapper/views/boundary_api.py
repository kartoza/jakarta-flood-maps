from flood_mapper.models.rw import RW
from flood_mapper.models.rt import RT
from flood_mapper.models.village import Village
from rest_framework.response import Response
from rest_framework import viewsets

from rest_framework.decorators import api_view

@api_view(['GET'])
def boundary_api(request, village, rw=None, rt=None):
    """
    API endpoint that allows users to be viewed or edited.
    """
    print village,rw,rt
    return Response('lala')
    # village = village.objects.filter(name='village')
    # if not village:
    #     return Response('')
    # if :
    #
    # queryset = RW.objects.all()
    # Response



