SHELL := /bin/bash

default: web

run: build web

deploy: run
	@echo
	@echo "--------------------------"
	@echo "Brining up fresh instance "
	@echo "--------------------------"
	#TODO - replace with something more precise
	@echo "Waiting 20 secs to ensure db is running"
	#@sleep 20
	@fig run -p jakartaflood uwsgi python manage.py migrate
	@fig run -p jakartaflood uwsgi python manage.py collectstatic --noinput

rm:
	@echo
	@echo "--------------------------"
	@echo "Killing production instance!!! "
	@echo "--------------------------"
	@fig  -p jakartaflood kill
	@fig  -p jakartaflood rm

web:
	@echo
	@echo "--------------------------"
	@echo "Running in production mode"
	@echo "--------------------------"
	@fig  -p jakartaflood up -d web
	@dipall

build:
	@echo
	@echo "--------------------------"
	@echo "Building in production mode"
	@echo "--------------------------"
	@fig  -p jakartaflood build

migrate:
	@echo
	@echo "--------------------------"
	@echo "Running migrate static in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood run uwsgi python manage.py migrate

collectstatic:
	@echo
	@echo "--------------------------"
	@echo "Collecting static in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood run uwsgi python manage.py collectstatic --noinput

kill:
	@echo
	@echo "--------------------------"
	@echo "Killing in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood kill

logs:
	@echo
	@echo "--------------------------"
	@echo "Showing uwsgi logs in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood logs uwsgi

nginxlogs:
	@echo
	@echo "--------------------------"
	@echo "Showing nginx logs in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood logs web

mapproxylogs:
	@echo
	@echo "--------------------------"
	@echo "Showing mapproxy logs in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood logs mapproxy

seed:
	@echo
	@echo "--------------------------"
	@echo "Seeding mapproxy in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood run mapproxy /usr/local/bin/mapproxy-seed -f /mapproxy/mapproxy.yaml /mapproxy/seed.yaml

shell:
	@echo
	@echo "--------------------------"
	@echo "Shelling in in production mode"
	@echo "--------------------------"
	@fig -p jakartaflood run uwsgi /bin/bash

dbshell:
	@echo
	@echo "--------------------------"
	@echo "Shelling in in production database"
	@echo "--------------------------"
	@docker exec -t -i jakartaflood_db_1 psql -U docker -h localhost gis

qgis:
	@echo
	@echo "--------------------------"
	@echo "Running QGIS desktop in production mode"
	@echo "Make sure you have started the services with make run first"
	@echo "--------------------------"
	@xhost +; docker run --rm --name="qgis-desktop-2-4" \
	-i -t \
	--link jakartaflood_db_1:db \
	--link jakartaflood_qgisserver_1:qgisserver \
	--link jakartaflood_mapproxy_1:mapproxy \
	--volumes-from jakartaflood_qgisserver_1 \
	-v ${HOME}:/home/$(USER) \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=unix$(DISPLAY) \
	kartoza/qgis-desktop:latest; xhost -

map:
	@echo
	@echo "--------------------------"
	@echo "Getting current 6 hour slot as pdf map"
	@echo "Make sure you have started the services with make run first"
	@echo "--------------------------"
	wget -O map.pdf "http://172.17.0.8/cgi-bin/qgis_mapserv.fcgi?map=/web/jk-floods.qgs&SERVICE=wms&LAYERS=Rw&REQUEST=GetPrint&TEMPLATE=6Hour&map0:EXTENT=11862318.594,-714081.378,11922154.957,-675870.096&map0:ROTATION=0&FORMAT=pdf&DPI=300"

#
# Staging
#
staging: stagingbuild stagingweb

stagingdeploy: stagingrun
	@echo
	@echo "--------------------------"
	@echo "Bringing up fresh staging instance "
	@echo "--------------------------"
	#TODO - replace with something more precise
	@echo "Waiting 20 secs to ensure db is running"
	@fig  -p jakartaflood -f fig-staging.yml run stagingweb python manage.py migrate
	@fig  -p jakartaflood -f fig-staging.yml run stagingweb python manage.py collectstatic --noinput

stagingrm:
	@echo
	@echo "--------------------------"
	@echo "Killing staging instance!!! "
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-staging.yml kill
	@fig -p jakartaflood -f fig-staging.yml rm

stagingweb:
	@echo
	@echo "--------------------------"
	@echo "Running in staging mode"
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-staging.yml up -d stagingweb

stagingbuild:
	@echo
	@echo "--------------------------"
	@echo "Building in staging mode"
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-staging.yml build

stagingmigrate:
	@echo
	@echo "--------------------------"
	@echo "Running migrate static in staging mode"
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-staging.yml run stagingweb python manage.py migrate

stagingcollectstatic:
	@echo
	@echo "--------------------------"
	@echo "Collecting static in staging mode"
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-staging.yml run stagingweb python manage.py collectstatic --noinput



# You need the production mode stuff in place
# before being able to use the dev stuff
# so we call build first
dev: build devssh devmigrate devcollectstatic

devkill:
	@echo
	@echo "-----------------------------------"
	@echo "Killing developer environment"
	@echo "-----------------------------------"
	@fig -p jakartaflood -f fig-dev.yml kill
	@fig -p jakartaflood -f fig-dev.yml rm

devdb:
	@echo
	@echo "-----------------------------------"
	@echo "Running db in developer mode"
	@echo "-----------------------------------"
	@fig -p jakartaflood -f fig-dev.yml up -d --no-recreate devdb

devdblogs:
	@echo
	@echo "-----------------------------------"
	@echo "Running db logs in developer mode"
	@echo "press ctrl-c to exit log watcher"
	@echo "-----------------------------------"
	@fig -p jakartaflood -f fig-dev.yml logs devdb

devssh:
	@echo
	@echo "--------------------------"
	@echo "Running ssh server in developer mode"
	@echo "You can attach to this as a remote interpreter"
	@echo "in pycharm."
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-dev.yml up -d --no-recreate dev

devmigrate:
	@echo
	@echo "--------------------------"
	@echo "Migrating in developer mode"
	@echo "--------------------------"
	@fig -p jakartaflood -f fig-dev.yml run dev /usr/local/bin/ manage.py migrate

devcollectstatic:
	@echo
	@echo "-----------------------------------"
	@echo "Collecting static in developer mode"
	@echo "-----------------------------------"
	@fig -p jakartaflood -f fig-dev.yml run dev /usr/local/bin/python manage.py collectstatic --noinput

devbuild: build
	@echo
	@echo "--------------------------"
	@echo "Building in developer mode"
	@echo "--------------------------"
	@fig -p jakartaflood build
	@fig -p jakartaflood -f fig-dev.yml build

devshell:
	@echo
	@echo "--------------------------"
	@echo "Starting shell in developer mode"
	@echo "--------------------------"
	@echo "Press enter to start your shell"
	@fig -p jakartaflood -f fig-dev.yml run dev /bin/bash
