from django.urls import path

from .views import NameEntryDetail, NameEntryList, UploadDictionaryView, UploadFormView

app_name = 'numerology'

urlpatterns = [
    path('', UploadFormView.as_view(), name='upload'),
    path('api/names/', NameEntryList.as_view(), name='name-list'),
    path('api/names/<int:pk>/', NameEntryDetail.as_view(), name='name-detail'),
    path('api/upload/', UploadDictionaryView.as_view(), name='upload-api'),
]
