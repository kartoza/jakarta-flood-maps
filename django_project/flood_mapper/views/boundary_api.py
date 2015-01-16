from flood_mapper.models.rw import RW, RWSerializer
from flood_mapper.models.rt import RT, RTSerializer
from flood_mapper.models.village import Village, VillageSerializer
from flood_mapper.models.flood_status import FloodStatus

from flood_mapper.utilities.utilities import get_time_slice

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def boundary_api(request, village=None, rw=None, rt=None):
    """
    API endpoint that allows users to be viewed or edited.
    """
    if rt:
        try:
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
            rw__village__id=int(village)).order_by('name')
        return Response(RTSerializer(matching_rts, many=True).data)
    elif village:
        matching_rws = RW.objects.filter(
            village__id=int(village)).order_by('name')
        return Response(RWSerializer(matching_rws, many=True).data)
    else:
        return Response(
            VillageSerializer(Village.objects.all(), many=True).data)


@api_view(['GET'])
def get_village_api(request, rw_id):
    try:
        rw = RW.objects.get(id=int(rw_id))
        village = rw.village
        return Response(VillageSerializer(village).data)
    except RW.DoesNotExist:
        return Response(None)


@api_view(['GET'])
def get_rw_by_id(request, rw_id):
    try:
        rw = RW.objects.get(id=int(rw_id))
        return Response(RWSerializer(rw).data)
    except RW.DoesNotExist:
        return Response(None)


@api_view(['GET'])
def boundary_flooded_api(request, time_slice='current', village=None):
    start_date_time, end_date_time = get_time_slice(time_slice)
    if village:
        flood_statuses = FloodStatus.objects.filter(
            date_time__gte=start_date_time,
            date_time__lte=end_date_time,
            rt__rw__village__id=village)
        rws = [
            flood_status.rt.rw for flood_status in flood_statuses]
        return Response(RWSerializer(rws, many=True).data)
    flood_statuses = FloodStatus.objects.filter(
        date_time__gte=start_date_time, date_time__lte=end_date_time)
    villages = [
        flood_status.rt.rw.village for flood_status in flood_statuses]
    return Response(VillageSerializer(villages, many=True).data)


@api_view(['GET'])
def all_flooded_rw(request, time_slice='current'):
    start_date_time, end_date_time = get_time_slice(time_slice)
    flood_statuses = FloodStatus.objects.filter(
        date_time__gte=start_date_time, date_time__lte=end_date_time)
    all_rws = set([flood_status.rt.rw.id for flood_status in flood_statuses])
    return Response(all_rws)
