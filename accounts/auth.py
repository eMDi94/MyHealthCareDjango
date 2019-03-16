from knox.auth import TokenAuthentication

from .models import User, Patient, Doctor


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        ret = super(CustomTokenAuthentication, self).authenticate(request)
        if ret is None:
            return None
        user, auth = ret
        if user.application_role == User.PATIENT:
            user = Patient.objects.get(user=user)
        else:
            user = Doctor.objects.get(user=user)
        if not user:
            return None
        return user, auth
