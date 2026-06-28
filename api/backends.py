from django.contrib.auth.backends import ModelBackend

from .models import User


class MultiFieldAuthBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, username=None, **kwargs):
        identifier = identifier or username
        if not identifier or not password:
            return None

        user = None

        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            pass

        if user is None:
            try:
                user = User.objects.get(phone=identifier)
            except User.DoesNotExist:
                pass

        if user is None:
            try:
                user = User.objects.get(tg_login=identifier)
            except User.DoesNotExist:
                pass

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
