from django.utils.translation import gettext_lazy as _

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView as DjRegisterView
from dj_rest_auth.views import UserDetailsView as DjUserDetailsView

from accounts.serializers import EmailChangeSerializer

from .models import CustomUser


class RegisterView(DjRegisterView):
    def get_response_data(self, user):
        return super().get_response_data(user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class EmailChangeView(UpdateAPIView):
    serializer_class = EmailChangeSerializer
    permission_classes = (IsAuthenticated,)

    def _change_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Email address changed")})

    def put(self, request, *args, **kwargs):
        return self._change_email(request)

    def patch(self, request, *args, **kwargs):
        return self._change_email(request)


class UserDetailsView(DjUserDetailsView):
    pass


# class DeleteUser(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
#     model = CustomUser
#     success_url = reverse_lazy("posts:home-view")
#     success_message = "Account deleted"
#     template_name = "accounts/confirm_delete.html"

#     def test_func(self):
#         user_obj = self.get_object()
#         return user_obj == self.request.user
