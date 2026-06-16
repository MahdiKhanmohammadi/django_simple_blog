from django.urls import path, include


urlpatterns = [
    path('', include("accounts.api.urls", namespace="accounts_api"))
]
