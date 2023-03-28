"""
Serializer file is specific for api's. Django is a framework for web development,
it means that Django is a package of many functionalities built-in that help developers
to create web applications. Even when Django is a framework for backend development, it allows us
to create the front end of our applications using Django templates and generic views. But in 
this case, out project uses a decoupled front-end built using Vuejs. The way to comunicate
a backend app with a decoupled frontend is using an api. An api is a set of endpoints that can be
used by the server to ask for information or to send information. This information is sent and received
as a JSON, however, this data is not usually formatted as expected, so we can use a serializer like
the one below to format data received. Other type of serializer is the model serializer, which maps 
JSON keys to Django model fields to avoid writing long chunks of code, since it does the mapping 
from keys to fields automatically.
"""

from rest_framework import serializers


class TransferSerializer(serializers.Serializer):
    """
    Serializer for initial parameters. Each parameters has its own
    data type:

    CharField = String
    IntegerField = Integer
    FloatField = Float

    None of the parameters is required to avoid errors with
    the request but still all of them can be received
    """

    initialAngle = serializers.FloatField(required=False)
    finalAngle = serializers.FloatField(required=False)
    angle = serializers.FloatField(required=False)
    steps = serializers.IntegerField(required=False)
    initialWaveLength = serializers.FloatField(required=False)
    finalWaveLength = serializers.FloatField(required=False)
    waveLength = serializers.FloatField(required=False)
    polarization = serializers.CharField(required=False)
    answer = serializers.CharField(required=False)
