#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on fedora
FROM kartoza/qgis-desktop:2.8.0
MAINTAINER Tim Sutton<tim@kartoza.com>

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN yum install -y cronie-anacron.x86_64 postgis.x86_64 xorg-x11-server-Xvfb.x86_64

ENV PYTHONPATH=$PYTHONPATH:/usr/share/qgis/python/
ADD crontab /etc/crontab
CMD ["crond", "-n"]
