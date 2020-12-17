from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'accounts'
urlpatterns = [
    # path('', TemplateView.as_view(template_name='main/welcome.html'), name='home'),
    path('', UserLoginView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', UserDashboardView.as_view(), name='dashboard'),
    path('viewstaff/', ListStaffView.as_view(), name='view-staff'),
    path('updatestaff/<int:pk>/', StaffUpdateView.as_view(), name='update-staff'),
    path('deletestaff/<int:pk>/', delete_staff, name='delete-staff'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('changepassword/', UserPasswordChangeView.as_view(), name='password_change'),
    path('passwordchanged/', UserPasswordChangeDoneView.as_view(), name='password_changed'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/<int:pk>', ProfileEditView.as_view(), name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
