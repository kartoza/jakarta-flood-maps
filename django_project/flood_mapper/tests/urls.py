from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^flood_mapper/', include('flood_mapper.urls', namespace='flood_mapper'))
)
