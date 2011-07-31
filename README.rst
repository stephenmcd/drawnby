`DrawnBy`_ is a collaborative drawing app built for the 2011 `Django Dash`_.
Users are able to create new drawings which anyone can contribute to in
real-time. Drawings can then be saved to the DrawnBy gallery where users
can view and vote on their favourite drawings.

Technical Overview
------------------

Aside from Django, DrawnBy brings together several unique technologies.
The `HTML5 canvas API`_, is used to implement client-side drawing features.
These interactions are then sent over the wire using `websockets`_
via `Socket.IO`_. `gevent`_ is used on the server to maintain long running
requests, and the key-value server `Redis`_ is used to store all drawing
interactions.

Installation
------------

DrawnBy was built on `Ubuntu`_ 10.04 provided by `Linode`_. The following
packages are required and can be installed via apt::

    sudo apt-get update
    sudo apt-get install build-essential
    sudo apt-get install python-pip
    sudo apt-get install python-imaging
    sudo apt-get install libevent-dev

Redis can be downloaded, built and run with the following commands::

    wget http://redis.googlecode.com/files/redis-2.2.12.tar.gz
    tar -xf redis-2.2.12.tar.gz
    cd redis-2.2.12
    sudo make
    ./src/redis-server

Development of DrawnBy is managed using the `Mercurial`_ version control
system and hosted on `BitBucket`_. With Mercurial installed, clone the
repository with the following command::

    hg clone http://bitbucket.org/stephenmcd/drawnby

The required Python packages can then be installed via `pip`_ with the
following command from the newly created ``drawnby`` project directory::

    cd drawnby
    sudo pip install -r requirements.txt

A database is then required. By default DrawnBy is configured for a SQLite
database. Consult the `django documentation`_ for configuring other
database servers. Once configured, the database can be created running the
following commands::

    python manage.py syncdb
    python manage.py migrate

To handle websockets, DrawnBy requires a custom server based on gevent.
As such a management command is provided to run the project::

    sudo python manage.py runserver_socketio

DrawnBy uses Twitter or Facebook to handle authentication. As such API
keys are required for an app with eithe provider. Once API keys are
obtained, rename the ``local_settings.py.template`` file in the ``drawnby``
project directory to ``local_settings.py`` and edit this file to set the
keys where defined.

.. _`DrawnBy`: http://drawnby.jupo.org/
.. _`Django Dash`: http://djangodash.com/
.. _`HTML5 canvas API`: http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html
.. _`websockets`: http://dev.w3.org/html5/websockets/
.. _`Socket.IO`: http://socket.io/
.. _`gevent`: http://www.gevent.org/
.. _`Redis`: http://redis.io/
.. _`Linode`: http://www.linode.com/
.. _`Ubuntu`: http://www.ubuntu.com/
.. _`Mercurial`: http://mercurial.selenic.com/
.. _`BitBucket`: https://bitbucket.org/
.. _`pip`: http://www.pip-installer.org/
.. _`django documentation`: https://docs.djangoproject.com/en/1.3/ref/databases/
