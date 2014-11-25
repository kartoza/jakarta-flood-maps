# Managing your docker deployed site

This document explains how to do various sysadmin related tasks when your 
site has been deployed under docker.

## Build your docker images and run them

You can simply run the provided script and it will build and deploy the docker
images for you in **production mode**.

``
fig build
fig up -d uwsgi
fig run collectstatic
fig run migrate
``

To create a staging site (or run any of the provided management scripts in 
staging mode), its the same procedure except you need to use the 
``fig-staging.yml`` environment variable e.g.::

``
fig -f fig-staging.yml build
fig -f fig-staging.yml up -d staginguwsgi
fig -f fig-staging.yml run stagingcollectstatic
fig -f fig-staging.yml run stagingmigrate
``

## Setup nginx reverse proxy

You should create a new nginx virtual host - please see 
``*-nginx.conf`` in the root directory of the source for an example. There is 
one provided for production and one for staging.

Simply add the example file to your ``/etc/nginx/sites-enabled/`` directory 
and then modify the contents to match your local filesystem paths. Then use

```
sudo nginx -t
```

To verify that your configuration is correct and then reload / restart nginx
e.g.

```
sudo /etc/init.d/nginx restart
```

## Management scripts

The following scripts are supplied:

### Create docker env

**Usage example:** ``fig build``

**Arguments:** [-f fig-dev.yml|fig-staging.yml]
 
**Description:** Running this script will create the docker images needed to
deploy your application. The -f argument is optional (if omitted, commands will
be run in production mode).

### Run in production mode

**Usage example:** ``fig up -d uwsgi``

**Arguments:** 

* ``-d`` - specifies that containers should be run in the background as daemons.

**Description:** Running this script will deploy your application in 
**production** mode. Note that we recommend running production mode in a 
separate checkout from your staging mode.

After creating the images (or fetching them if they are being used from 
the docker hub repository), container instances will be deployed and you should
then do any initialisation that needs to be carried out (
e.g. migrations, collect static) see below for details.

Once the command is run, you should see a number of docker containers running
and linking to each other when you run the ``docker ps`` command. You 
should also be able to visit the site in your web browser after ensuring that
your nginx proxy configuration is correct (see above).

### Run in staging mode

**Usage example:** ``fig -f fig-staging.yml up -d staginguwsgi``

**Arguments:** 
* ``-f`` - specifies that the fig staging config should be used.
* ``-d`` - specifies that containers should be run in the background as daemons.

**Description:** Running this script will deploy your application in staging 
mode. Note that we recommend running staging mode in a separate checkout.

After creating the images (or fetching them if they are being used from 
the docker hub repository), container instances will be deployed and you should
then do any initialisation that needs to be carried out (
e.g. migrations, collect static) see below for details.

Once the command is run, you should see a number of docker containers running
and linking to each other when you run the ``docker ps`` command. You 
should also be able to visit the site in your web browser after ensuring that
your nginx proxy configuration is correct (see above).


### Collect static

**Usage:** ``fig [-f fig-staging.yml] <collectstatic|stagingcollectstatic>``

**Example Usage:** 

* ``fig collectstatic``
* fig [-f fig-staging.yml stagingcollectstatic

**Arguments:** 
* ``-f`` - specifies that the fig staging config should be used.
* ``-d`` - specifies that containers should be run in the background as daemons.
 
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run 

```django manage.py collectstatic --noinput --settings=core.settings.prod_docker```

or 

```django manage.py collectstatic --noinput --settings=core.settings.staging_docker```

Depending on whether you supply the 

### Run migrations


**Usage example:** ``scripts/run_migrations_docker.sh``

**Arguments:** None
* ``-f`` - specifies that the fig staging config should be used.

 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run this command inside
the container:

```django manage.py migrate --settings=core.settings.prod_docker```

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/run_migrations_docker.sh``


### Bash prompt

**Usage example:** ``scripts/docker_bash.sh``

**Arguments:** None
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will start an interactive bash
shell inside the container that you can use to run ad hoc commands with 
the django project context and database connection available. 

**Test mode support?:** Yes. See section above on **Create docker env** for more details 
prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/docker_bash.sh``


### Management commands

**Usage example:** ``scripts/manage.sh``

**Arguments:** Arbitrary django management command options are supported e.g. 

``scripts/manage.sh --help`` 

will invoke the django management command help. There is no need to use the
``--settings`` option unless you want to override it since this option is 
automatically passed in as ``DJANGO_SETTINGS_MODULE=core.settings.prod_docker``.
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run this command inside
the container:

```django manage.py <your parameters>```

After running the management command the container will be destroyed.

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/manage.sh --help``

### Restart django

**Usage example:** ``scripts/restart_django_server.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
django uwsgi container, and then restart it. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive.

If you need to deploy changes to your django application (e.g. adding some 
new python dependency), the general workflow is:

* rebuild your production image (``cd docker-prod; .build.sh; cd -``)
* restart your production container (``scripts/restart_django_server.sh``)

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/restart_django_server.sh``

### Run django development server

**Usage example:** ``scripts/run_django_dev_server.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
django development container, and then restart it. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive.

If you need to deploy changes to your django application (e.g. adding some 
new python dependency), the general workflow is:

* rebuild your development image (``cd docker-dev; .build.sh; cd -``)
* restart your development container (``scripts/run_django_dev_server.sh``)

When the development container starts, it will launch sshd which you can connect
to using the credentials:

* **User:** docker
* **Password:** docker

Please see README-dev.md for more details on how to use this development
container for efficient development from within PyCharm.

**Test mode support?:** No

``TEST_MODE=1 scripts/restart_django_server.sh``

### Run QGIS desktop

**Usage example:** ``scripts/run_qgis_desktop.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
QGIS desktop container, and then restart it. It will mount your the ``webmaps``
directory from in your code tree under ``/web`` in the container via a docker 
shared volume and create a link to your database, using docker's ``--link`` 
directive.


**Test mode support?:** Currently unsupported! The main issue is that
QGIS project files cannot honour the environmentals which are used to 
define the PostgreSQL connection details. So our recommendation is that you
run a copy of the production mode environment on your local machine when you
are building out QGIS projects against the docker service.


# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing 
``scripts/config.sh``.
