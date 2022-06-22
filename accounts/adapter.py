from allauth.account.adapter import DefaultAccountAdapter


# Fixes bug between dj rest auth and allauth where allauth adds
# sessionid cookie even if REST_USE_JWT is true
class AccountAdapter(DefaultAccountAdapter):
    def login(self, request, *args, **kwargs):
        request.session.flush()
