.. raw:: html

    <div align="center">
      <h1>EvPhoto</h1>
    </div>

|Python Version| |Contributions Welcome| |License|

.. |Python Version| image:: https://img.shields.io/badge/python-v3.7+-blue.svg
   :target: http://shields.io/
.. |Contributions Welcome| image:: https://img.shields.io/badge/contributions-welcome-orange.svg
   :target: http://shields.io/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT


Capture an image and display it to a web page.


Installation
============
Note: The following installations instructions have been tested only in Ubuntu 20.04

Before you are ready to run EvPhoto, ensure you have ``Python 3.7`` or later on your system as well the latest pip version. We recommend to run EvPhoto within a python virtual environment for easier management. If you don't have a virtual environment already created, create a new one by issuing the following commands within a directory of your choice:

.. code-block:: bash

    python3 -m venv pyenv
    source pyenv/bin/activate

Within the directory where you wish to install EvPhoto, download the latest source code using git:

.. code-block:: bash

    git clone git://github.com/raikel/evphoto.git

Or download it manually. After that, cd into the project directory and install python dependencies:

.. code-block:: bash

    cd evphoto
    pip install requirements.txt
    
Next, create database migrations and start the local server:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    
Access the application at `http://localhost:8000`.

REST API
========

The base url of the REST API is ``http://localhost:8000/api``. The API documentation can 
be accessed at ``http://localhost:8000/api/docs/swagger/`` (in swagger format) or
at ``http://localhost:8000/api/docs/redoc/`` (in redoc format)

Admin interface
========

To access the admin interface, you must create first ad admin user with:

.. code-block:: bash

    python manage.py createsuperuser
    
Then you can access the admin interface at ``http://localhost:8000/admin``

Deployment
==========

To deploy in production, first install Ansible in your system. 

.. code-block:: bash

    sudo apt install python3-wheel python3-pip python3-apt
    sudo apt install ansible

    
Next cd into the deploy directory on the project root and copy the 
template configuration file in ``group_vars/all_.yml`` to 
``group_vars/all.yml``. Next, make the necessary changes to this file
to define your required deployment options. You must define all the 
variables with a default value enclosed by ``<>``.

.. code-block:: bash

    cp group_vars/all_.yml group_vars/all.yml
    nano group_vars/all.yml # Edit required variables here

Finally, deploy the project with

.. code-block:: bash

    bash deploy.sh
