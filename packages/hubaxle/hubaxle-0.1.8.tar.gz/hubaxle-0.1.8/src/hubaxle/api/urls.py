from django.urls import path, include
from .views import SecretViewListCreate, CameraConfigViewList, ConfigEntryViewRetrieveUpdate

urlpatterns = [
    path("secrets", SecretViewListCreate.as_view(), name="secrets-list-create"),
    path("appdata/app/appconfig", ConfigEntryViewRetrieveUpdate.as_view(), name="appconfig-retrieve-update"),
    path("cameras", CameraConfigViewList.as_view(), name="camera-list")
]
