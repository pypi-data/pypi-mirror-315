from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin

from .serializers import SecretSerializer, CameraConfigSerializer
from .models import Secret, CameraConfig
from hubaxle.cfgstore.serializers import ConfigEntrySerializer
from hubaxle.cfgstore.models import ConfigEntry

class SecretViewListCreate(LoginRequiredMixin, ListCreateAPIView):
    serializer_class = SecretSerializer
    raise_exception = True

    @extend_schema(
        operation_id="list secrets",
        description="List all secrets in the hub",
        tags=["secrets"],
        responses={status.HTTP_200_OK: SecretSerializer(many=True)}
    )
    def get(self, request):
        secrets = Secret.objects.all()
        serializer = self.serializer_class(secrets, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        operation_id="create secret",
        description="Create a secret in the hub",
        tags=["secrets"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({}, status=400)


# TODO: apps should each be their own user. We can then authenticate based on user and make sure each app can have their own app config, and use the LoginRequiredMixin
# For now we only support a single app
class ConfigEntryViewRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = ConfigEntrySerializer
    raise_exception = True

    # TODO: replace this to support multiple apps having their own configs. With only one config, this function always gets the same object
    def get_object(self):
        try:
            config = ConfigEntry.objects.get(name="app_config")
        except ConfigEntry.DoesNotExist:
            config = ConfigEntry.objects.create(name="app_config", kind="yaml", contents="")
        return config

    @extend_schema(
        operation_id="get app config",
        description="Get the app configuration, returned as a binary stream",
        tags=["app_data"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="put app config",
        description="put the app configuration",
        tags=["app_data"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="patch app config",
        description="patch the app configuration",
        tags=["app_data"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# TODO: Big TODOs around enabling multiple apps. Not all apps should get all cameras, and we should have a way to authenticate the apps
# For now, with one app (SMT) we can just provide all the cameras
class CameraConfigViewList(ListModelMixin, GenericAPIView):
    serializer_class = CameraConfigSerializer
    raise_exception = True

    # TODO: replace this if we want to limit the cameras retrieved
    def get_queryset(self):
        return CameraConfig.objects.filter()

    @extend_schema(
        operation_id="list cameras",
        description="list all cameras",
        tags=["cameras"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request=request, args=args, kwargs=kwargs)