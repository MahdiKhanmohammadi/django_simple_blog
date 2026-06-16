from django.urls import path
from .views import RegisterUserGenericApiView, ActivateUserWithVerifyCodeApiView, DestroyCurrentUserTokenApiView
from rest_framework.authtoken.views import ObtainAuthToken

app_name = "accounts_api"

urlpatterns = [
    path('register/', RegisterUserGenericApiView.as_view(), name="register"),
    path('generate-token/', ObtainAuthToken.as_view(), name='generate_token'),
    path("active/<verify_code>/", ActivateUserWithVerifyCodeApiView.as_view(),
         name='active_account'),
    path('destroy-token/', DestroyCurrentUserTokenApiView.as_view(),
         name='destroy_token')

]
