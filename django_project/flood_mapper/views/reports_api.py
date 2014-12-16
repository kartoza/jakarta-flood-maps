from flood_mapper.models.rw import RW, RWSerializer
from flood_mapper.models.flood_status import (
    FloodStatus,
    FloodStatusSerializer,
    FloodStatusFullSerializer
)
from flood_mapper.models.rt import RT, RTSerializer
from flood_mapper.models.village import Village, VillageSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view

@api_view(['GET'])
def reports_rw_api(request, rw_id):
    """
    Get a report associated with a rw
    """
    flood_status_reports = FloodStatus.objects.filter(rt__rw__id=int(rw_id))

    if 1:  # TODO: Logged in user
        return Response(
            FloodStatusSerializer(flood_status_reports, many=True).data)
    else:
        return Response(
            FloodStatusFullSerializer(flood_status_reports, many=True).data)

