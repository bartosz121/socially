from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView

from dj_rest_auth.registration.views import RegisterView as DjRegisterView

from .models import CustomUser


class RegisterView(DjRegisterView):
    def get_response_data(self, user):
        return super().get_response_data(user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class DeleteUser(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy("posts:home-view")
    success_message = "Account deleted"
    template_name = "accounts/confirm_delete.html"

    def test_func(self):
        user_obj = self.get_object()
        return user_obj == self.request.user
