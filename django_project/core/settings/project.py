# -*- coding: utf-8 -*-
from .contrib import *  # noqa

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': '',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Project apps
INSTALLED_APPS += (
    'flood_mapper',
)


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.1.min.js',
            'js/bootstrap.js',
            'js/moment.min.js',
            'flood_mapper/js/leaflet.js',
            'flood_mapper/js/material.min.js',
            'flood_mapper/js/ripples.min.js',
            'flood_mapper/js/validate.js',
            'js/bootstrap-datetimepicker.min.js',
        ),
        'output_filename': 'js/contrib.js',
    },
    'appjs': {
        'source_filenames': (
            'js/csrf-ajax.js',
            'flood_mapper/js/jakarta-flood-maps.js',
        ),
        'output_filename': 'js/appjs.js'
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.min.css',
            'flood_mapper/css/leaflet.css',
            'flood_mapper/css/material-wfont.min.css',
            'flood_mapper/css/ripples.min.css',
            'flood_mapper/css/bnpb-theme.css',
            'css/bootstrap-datetimepicker.min.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}
