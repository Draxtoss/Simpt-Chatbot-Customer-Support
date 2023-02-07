from django.shortcuts import render
from intents.serializers import IntentsWithoutIDSerializer,IntentsSerializer,UnIdentifiedSerializer
from intents.models import Intents,Unidentified
from rest_framework import viewsets,status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from intents.training_model import chat
# Create your views here.
class IntentsViewSet(viewsets.ModelViewSet):
    queryset = Intents.objects.all()
    serializer_class = IntentsWithoutIDSerializer
    def get_serializer(self, *args, **kwargs):
        # add many=True if the data is of type list
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(IntentsViewSet, self).get_serializer(*args, **kwargs)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        chat()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
class IntentsIDViewSet(viewsets.ModelViewSet):
    queryset = Intents.objects.all()
    serializer_class = IntentsSerializer
    def get_serializer(self, *args, **kwargs):
        # add many=True if the data is of type list
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(IntentsIDViewSet, self).get_serializer(*args, **kwargs)
class UnidentifiedMessagesViewSet(viewsets.ModelViewSet):
    queryset = Unidentified.objects.all()
    serializer_class = UnIdentifiedSerializer
    def get_serializer(self, *args, **kwargs):
        # add many=True if the data is of type list
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(UnidentifiedMessagesViewSet, self).get_serializer(*args, **kwargs)