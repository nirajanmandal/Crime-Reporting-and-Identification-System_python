from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'detection'
urlpatterns = [
    path('detectimage/', detect_image, name='detect-image'),
    path('detectwithwebcam/', detect_with_webcam, name='detect-webcam'),
    path('adduser/', add_staff, name='add-user'),
    path('addcitizen/', AddCitizen.as_view(), name='add-citizen'),
    path('viewcitizen/', ListCitizenView.as_view(), name='view-citizen'),
    path('deletecitizen/<int:pk>/', delete_citizen, name='delete-citizen'),
    path('updatecitizen/<int:pk>/', UpdateCitizenView.as_view(), name='update-citizen'),
    path('downloadcsvfile/<int:pk>/', csv_database_write, name='download-csv-file'),
    path('upload/', FileView, name='file-upload'),
    path('spottedcitizen/', SpottedCitizenView.as_view(), name='spotted-citizen'),
    path('citizenlocation/<int:pk>', citizen_location, name='citizen-location'),
    path('foundcitizen/<int:pk>/', found_citizen, name='found-citizen'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
