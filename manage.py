#!/usr/bin/env python

"""
This file allows the execution of all the commands related to Django.
Every command starts with:
python manage.py ...

Some of them are:
python manage.py runserver - To run locally the backend
python manage.py createsuperuser - To create a super user that can access to the Django admin screens
python manage.py makemigrations - To create the files with all the changes to be executed on the DB according
to the changes on the models.py files.
python manage.py migrate - To apply on DB all the changes captured on the migrations files
"""
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # app directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "app"))

    execute_from_command_line(sys.argv)
