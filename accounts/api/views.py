from rest_framework.views import APIView
from .serializer import UserModelSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from accounts.tasks import send_email
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.request import HttpRequest
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView


class RegisterUserGenericApiView(GenericAPIView):
    serializer_class = UserModelSerializer

    def post(self, request: HttpRequest):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email_user = serializer.validated_data.get('email')
            get_password = serializer.validated_data.get('password')
            UserModel = get_user_model()
            get_user = UserModel(email=email_user)
            get_user.set_password(get_password)
            get_user.save()
            print(get_user.email)

            active_account_path = request.build_absolute_uri(reverse("accounts_api:active_account", kwargs={
                'verify_code': get_user.verify_code}))

            send_email.delay(get_user.email, active_account_path)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.error_messages, status=HTTP_400_BAD_REQUEST)


class ActivateUserWithVerifyCodeApiView(APIView):
    def get(self, request, verify_code):
        UserModel = get_user_model()
        try:
            get_user = UserModel.objects.get(verify_code=verify_code)
        except:
            get_user = None

        if get_user:
            get_user.is_active = True
            get_user.save()
            return Response(data={'detail': True}, status=HTTP_200_OK)
        else:
            return Response(data={"detail": "notfound"}, status=HTTP_404_NOT_FOUND)


class DestroyCurrentUserTokenApiView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request: HttpRequest):
        current_user = request.user
        current_user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)
