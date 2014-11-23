#!/bin/bash
ORGANISATION=kartoza
PROJECT=jakarta-flood-maps
PG_USER=docker
PG_PASS=docker
BASE_PORT=1719
# This also need to be configured in the dockerfile
# The uwsgi file and nginx conf	
DJANGO_UWSGI_INTERNAL_PORT=1721
