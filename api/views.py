from django.shortcuts import render

from dj_rest_auth.registration.views import RegisterView as DjRegisterView


class RegisterView(DjRegisterView):
    def get_response_data(self, user):
        print("get response data")
        return super().get_response_data(user)

    def create(self, request, *args, **kwargs):
        print("create")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("perform create")
        return super().perform_create(serializer)
