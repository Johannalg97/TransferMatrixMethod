"""
This file allows Django to recognize the folder 'api'
as an application of the project. The file /config/settings/base.py
calls this file from the LOCAL_APPS variable, where all the local 
applications are loaded 
"""

from django.apps import AppConfig


# Configuration needed to allow Django to use this application
# called api
class ApiConfig(AppConfig):
    name = "app.api"
