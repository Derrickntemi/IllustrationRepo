from django.shortcuts import render
from .models import Articles
from .decorators import validate_request
from .serializers import ArticlesSerializer, TokenSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView


class ListCreateArticlesView(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer


permission_classes = (permissions.IsAuthenticated)


@validate_request
def post(self, request, *args, **kwargs):
    article = Articles.objects.create(
        title=request.data["title"],
        author=request.data["author"]
    )
    return Response(
        data=ArticlesSerializer(article).data,
        status=status.HTTP_201_CREATED
    )

  # GET,PUT,DELETE
class ArticlesDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

    def get(self, request, *args, **kwargs):
        try:
            article = self.queryset.get(pk=kwargs["pk"])
            return Response(ArticlesSerializer(article).data)
        except Articles.DoesNotExist:
            return Response(
                data={
                    "message": f"Article id: {kwargs['pk']} doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request
    def put(self, request, *args, **kwargs):
        try:
            article = self.queryset.get(pk=kwargs["pk"])
            serializer = ArticlesSerializer()
            updated_article = serializer.update(article, request.data)
            return Response(ArticlesSerializer(updated_article).data)
        except Articles.DoesNotExist:
            return Response(
                data={
                    "message": f"Article id: {kwargs['pk']} doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            article = self.queryset.get(pk=kwargs["pk"])
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Articles.DoesNotExist:
            return Response(
                data={
                    "message": f"Article id: {kwargs['pk']} doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )

# login
# This permission class will override the global permission


# Retrieve the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(APIView): #can use generics.CreateApiView

    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # utilizing drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

# user registration


class RegisterUsers(APIView):  # can use generics.CreateApiView

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

# GET,PUT,DELETE


class UsersDetailView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(pk=kwargs["pk"])
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": f"User id: {kwargs['pk']} doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
