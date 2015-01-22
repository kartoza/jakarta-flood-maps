#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/qgis-server
MAINTAINER Tim Sutton<tim@kartoza.com>

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get update -y; apt-get -y --force-yes install cron postgis

# For deployment:
# Mount the directories when running this volume
#    - ../maps:/home/web/maps
#    - ./reports:/home/web/reports
#    - ./cron-scripts:/home/web/cron-scripts
ADD crontab /etc/crontab
CMD ["cron", "-f"]
