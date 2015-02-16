#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on fedora
FROM kartoza/qgis-desktop:2.6.1
MAINTAINER Tim Sutton<tim@kartoza.com>

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN yum install -y cronie-anacron.x86_64 postgis.x86_64 xorg-x11-server-Xvfb.x86_64

# For deployment:
# Mount the directories when running this volume
#    - ../maps:/home/web/maps
#    - ./reports:/home/web/reports
#    - ./cron-scripts:/home/web/cron-scripts

WORKDIR /tmp
RUN yum install -y wget; \
    wget http://corefonts.sourceforge.net/msttcorefonts-2.5-1.spec; \
    yum install -y rpm-build cabextract ttmkfdir
RUN rpmbuild -bb msttcorefonts-2.5-1.spec
RUN yum install -y /root/rpmbuild/RPMS/noarch/msttcorefonts-2.5-1.noarch.rpm


ENV PYTHONPATH=$PYTHONPATH:/usr/share/qgis/python/
ADD crontab /etc/crontab
CMD ["crond", "-n"]
