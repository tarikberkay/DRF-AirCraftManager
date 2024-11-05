from django.urls import path
from authentication.views import (
    LoginTokenView,
    RegisterView,
    ChangePasswordView,
    # logout_view,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "authentication"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginTokenView.as_view(), name="login-token"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
