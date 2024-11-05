from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from drf_spectacular.utils import (
    extend_schema, inline_serializer, OpenApiParameter, OpenApiTypes)
from django.contrib.auth import get_user_model

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from authentication.rest.serializers import UserRegisterSerializer
from authentication.rest.serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from aircraft.models import Team


class LoginTokenView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Login Token",
        description="Login Token",
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if "access" in response.data:
            jwt_authenticator = JWTAuthentication()
            validated_token = jwt_authenticator.get_validated_token(
                response.data.get("access"))
            user_id = validated_token.get("user_id")
            user = get_user_model().objects.get(id=user_id)
            serializer = UserRegisterSerializer(instance=user)
            response.data.update(serializer.data)
        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    @extend_schema(
        tags=["Authentication"],
        request=inline_serializer(
            name="Register",
            fields={
                'name': serializers.CharField(required=True),
                'email': serializers.EmailField(required=True),
                'password': serializers.CharField(required=True),
                'phone': serializers.CharField(required=True),
                'is_personel': serializers.BooleanField(required=True),
                'team': serializers.IntegerField(required=False)
            }
        ),
        responses={201: UserRegisterSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        password = request.data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"password": list(e.messages)},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.save(
                name=request.data.get('name'),
                phone=request.data.get('phone'),
                team_id=request.data.get('team')
            )

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        tags=["Authentication"],
        summary="Change Password",
        description="Change the password for the authenticated user.",
        request=ChangePasswordSerializer,
        responses={200: {"message": "Password changed successfully."}},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        new_password = request.data.get('new_password')

        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response({"new_password": list(e.messages)},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            update_session_auth_hash(request, request.user)
            return Response(
                {"message": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)