# Welcome to the django wms client code base!

**jakarta-flood-maps** is a django app that will allow you to embed maps 
via the Open Geospatial Consortium Web Mapping Service (OGC-WMS or just WMS)
into your django application.

Please note that this is an early version and so may not be ready for your 
needs yet.

# Status

These badges reflect the current status of our development branch:

Tests status: [![Build Status](https://travis-ci.org/kartoza/jakarta-flood-maps.svg)](https://travis-ci.org/kartoza/jakarta-flood-maps)

Coverage status: [![Coverage Status](https://coveralls.io/repos/kartoza/jakarta-flood-maps/badge.png?branch=develop)](https://coveralls.io/r/kartoza/jakarta-flood-maps?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/kartoza/jakarta-flood-maps.svg?label=ready&title=Ready)](http://waffle.io/kartoza/jakarta-flood-maps) [![Stories in Progress](https://badge.waffle.io/kartoza/jakarta-flood-maps.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/kartoza/jakarta-flood-maps)

# License

Code: [BSD License](http://www.freebsd.org/copyright/freebsd-license.html)


# Setup instructions

1. First jakarta-flood-maps with pip:

   ```
    pip install jakarta-flood-maps
   ```

2. Next include it in ``INSTALLED_APPS`` in your settings.py:
   ```
    INSTALLED_APPS = (
        ...
        'flood_mapper',
    )
   ```

3. Add the wms-client URLconf in your project urls.py e.g:
   ```
    url(r'^wms-client/', include('flood_mapper.urls')),
   ```

4. Run ```python manage.py migrate``` to create the flood_mapper models. 

5. Visit http://127.0.0.1:8000/wms-client/ to open the app.

6. Visit your admin page (the default is http://127.0.0.1:8000/admin/wms-maps) 
  to manage user as an admin. 


Testing
--------

You can run the test suite by using django manage.py from your django project:

```
python manage.py test flood_mapper
```

or you can do it from the root of this django apps by running:
```
python setup.py test
```

