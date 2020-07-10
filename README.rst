cdsso.codedevils.org
====================

Identity Access Manager (IAM) user weblogin for CodeDevils, offering CAS 3.0 protocol to log
users into CodeDevils applications.

.. image:: https://travis-ci.com/ASU-CodeDevils/cdsso.svg?token=FhsGC7ZUMb7rskmp3jDy&branch=master
    :target: https://travis-ci.com/ASU-CodeDevils/cdsso
    :alt: Build
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/badge/chat-slack-pink.svg
    :target: https://codedevils.slack.com/archives/GPNBSDM27
    :alt: Slack

Website Status
--------------

Production
^^^^^^^^^^

.. image:: https://travis-ci.com/ASU-CodeDevils/cdsso.svg?token=FhsGC7ZUMb7rskmp3jDy&branch=master
    :target: https://travis-ci.com/github/ASU-CodeDevils/cdsso
    :alt: Build
.. image:: https://img.shields.io/uptimerobot/status/m784417521-1b9dcabb76b05ae6fdc099b3
    :target: https://sso.codedevils.org
    :alt: Status (prod)
.. image:: https://img.shields.io/uptimerobot/ratio/m784417521-1b9dcabb76b05ae6fdc099b3
    :target: https://status.codedevils.org/784417521
    :alt: Uptime (prod)

QA
^^

.. image:: https://travis-ci.com/ASU-CodeDevils/cdsso.svg?token=FhsGC7ZUMb7rskmp3jDy&branch=dev
    :target: https://travis-ci.com/github/ASU-CodeDevils/cdsso
    :alt: Build
.. image:: https://img.shields.io/uptimerobot/status/m784417527-57e543ec1e2e0752a9ba2228
    :target: https://qa-sso.codedevils.org
    :alt: Status (QA)
.. image:: https://img.shields.io/uptimerobot/ratio/m784417527-57e543ec1e2e0752a9ba2228
    :target: https://status.codedevils.org/784417527
    :alt: Uptime (QA)

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy cdsso

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd codedevils_org
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Deployment
----------

The following details how to deploy this application.
