

from flood_mapper.models.flood_status import (
    FloodStatus,
    FloodStatusSerializer
)
from rest_framework.response import Response

from rest_framework.decorators import api_view

@api_view(['GET'])
def reports_rt_api(request, rt_id):
    """
    Get a report associated with a rw
    """
    flood_status_reports = FloodStatus.objects.filter(rt__id=int(rt_id))
    return Response(
        FloodStatusSerializer(flood_status_reports, many=True).data)
