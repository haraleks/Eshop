======================
Backend is project online store
======================

Swagger on url: `/swagger/`, `/swagger.json`

RESTful API online store for the sale of phones


* Install `docker <https://docs.docker.com/engine/install/>`_

* Install docker-compose:

   `pip install docker-compose`


* Clone project:

    `cd /path/to/project`

***************
How start?
***************

* Start the environment (it will take a long time to build for the first time):

    `make run`

* Stoped:

    `make stop`

***************
How enter?
***************

Open browser: `0.0.0.0:8000 <http://0.0.0.0:8000>`_

****************
How test?
****************

    `make test`


***************************
If there are problems with migrations?
***************************

    `make clean`

*****************************************
The rest of the commands can be found by running:
*****************************************

    `make`

______________________________________________________________________________

*****************************************
Main modules project:
*****************************************

Eshop
~~~~~~~~~~~~~~~~~

1. env files all settings

Apps
~~~~~~~~~~~~~~~~~
1. shop - keep main module on project
2. User - keep module registration customer
3. core - auxiliary functions

