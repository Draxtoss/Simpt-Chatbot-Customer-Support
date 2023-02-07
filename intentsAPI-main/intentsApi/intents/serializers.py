from http.client import responses
from rest_framework import  serializers
from intents.models import Intents,Unidentified 
# Serializers define the API representation.
class IntentsWithoutIDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Intents
        fields = ['tag','patterns','responses']

class IntentsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Intents
        fields = ['id','tag','patterns','responses']

class UnIdentifiedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unidentified
        fields = ['messages']