=====
Usage
=====

TODO: Modify this template in wooyek/cookiecutter-django-website for django project installation


To use Picropper in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'picropper.apps.PicropperConfig',
        ...
    )

Add Picropper's URL patterns:

.. code-block:: python

    from picropper import urls as picropper_urls


    urlpatterns = [
        ...
        url(r'^', include(picropper_urls)),
        ...
    ]
