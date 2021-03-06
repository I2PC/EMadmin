#!/usr/bin/env python
# sudo fuser -k 8000/tcp
import os
import sys

if __name__ == "__main__":
    # CHANGED manage.py will use development settings by
    # default. Change the DJANGO_SETTINGS_MODULE environment variable
    # for using the environment specific settings file.
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EMadmin.settings.development")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EMadmin.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
