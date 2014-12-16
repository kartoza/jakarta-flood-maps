from flood_mapper.models.rw import RW, RWSerializer
from flood_mapper.models.rt import RT, RTSerializer
from flood_mapper.models.village import Village, VillageSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view

@api_view(['GET'])
def boundary_api(request, village=None, rw=None, rt=None):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if rt:
        try:
            print type(rt), rw, village
            matching_rt = RT.objects.get(
                id=int(rt),
                rw__id=int(rw),
                rw__village__id=int(village))
            return Response(RTSerializer(matching_rt).data)
        except RT.DoesNotExist:
            return Response(None)
    elif rw:
        if not village:
            return Response(None)
        matching_rts = RT.objects.filter(
            rw__id=int(rw),
            rw__village__id=int(village))
        return Response(RTSerializer(matching_rts, many=True).data)
    elif village:
        matching_rts = RW.objects.filter(
            village__id=int(village))
        return Response(RWSerializer(matching_rts, many=True).data)
    else:
        return Response(
            VillageSerializer(Village.objects.all(), many=True).data)
