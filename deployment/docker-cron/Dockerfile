#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on fedora
FROM kartoza/qgis-desktop:2.8.0
MAINTAINER Tim Sutton<tim@kartoza.com>

RUN yum install -y cronie-anacron.x86_64 postgis.x86_64 xorg-x11-server-Xvfb.x86_64

ENV PYTHONPATH=$PYTHONPATH:/usr/share/qgis/python/
ADD crontab /var/spool/cron/root
CMD ["crond", "-n"]
