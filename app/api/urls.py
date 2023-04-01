"""
This file represents the set of endpoints that our api has. Each endpoint
or url is the first parameter on the path() statement. Complete url is built as follows:

app domain + api application url + endpoint

If the project is running locally and we are trying to download data from a graph
the complete URL would be like:

http://127.0.0.1:8000/api/v1/download-data/

Where 127.0.0.1 is the localhost, 8000 is the port used, /api/v1/ is the prefix for
all of the urls cointained in this file of api urls, and download-data/ is the current
endpoint we are trying to send information to.

Once the browser (named also client) sends a request to the server (to Django),
Django will look for a url that matches the url that the user is sending to us.
Once it finds the url, Django will execute the view related to that url. In the example
above, the DownloadDataView would be executed.

"""


from django.urls import include, path

from app.api import views

# Name of this app (folder api) inside of the whole project (folder app)
app_name = "api"

urlpatterns = [
    # URL to receive post data from browser with all the information from the materials
    # and initial parameters. Once the request is received, the view CalculateDataView is
    # going to process it.
    path("transfer-method/", views.CalculateDataView.as_view(), name="calculate"),
    path("download-data/", views.DownloadDataView.as_view(), name="download"),
    path(
        "calculate-chi/",
        views.CompareExperimentalDataView.as_view(),
        name="compare_experimental_data",
    ),
]

