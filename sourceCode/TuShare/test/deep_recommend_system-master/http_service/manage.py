#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "restful_server.settings")

    from django.core.management import execute_from_command_line
    
    print(sys.argv)

    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8080'])
