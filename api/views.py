from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Event
from .serializers import EventSerializer, PostEventSerializer


@api_view(["GET", "POST"])
def event_collection(request):
    if request.method == "GET":
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)

    serializer = PostEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "PUT", "DELETE"])
def event_element(request, pk):
    if request.method == "PUT":
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(instance=event, data=request.data)
        except Event.DoesNotExist:
            serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(pk=pk)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = EventSerializer(event)

        return Response(serializer.data)

    if request.method == "DELETE":
        event.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCH":
        serializer = EventSerializer(instance=event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
