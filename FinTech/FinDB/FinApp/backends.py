from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user is not None and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
