from .models import Profile


def get_staff(request):
    staff = Profile.objects.all()
    return {
        'staff': staff
    }

