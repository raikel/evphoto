from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer
from .services import take_photo


class PhotoView(viewsets.GenericViewSet):
    lookup_field = 'pk'
    model_name = 'Photo'
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def create(self, request):
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            data=request.data,
            context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        image_name, temperature, error = take_photo()

        photo = Photo.objects.create(
            session=serializer.data['session'],
            side=serializer.data['side'],
            temperature=temperature,
            error=error,
            image=image_name,
        )

        serializer = self.serializer_class(
            photo,
            context=serializer_context
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        fields = request.query_params.get('fields', None)
        if fields is not None:
            fields = fields.split(',')

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True,
            fields=fields
        )
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            pk = int(pk)
            instance = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(f'A {self.model_name} with pk={pk} does not exist.')

        instance.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        serializer_context = {'request': request}
        try:
            pk = int(pk)
            instance = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(f'A {self.model_name} with pk={pk} does not exist.')

        fields = request.query_params.get('fields', None)
        if fields is not None:
            fields = fields.split(',')

        serializer = self.serializer_class(
            instance,
            context=serializer_context,
            fields=fields
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
