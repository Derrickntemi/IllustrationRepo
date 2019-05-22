from rest_framework import serializers
from .models import Articles
from django.contrib.auth.models import User

#marshalls and unmarshalls the Article
class ArticlesSerializer (serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ("title","author")

   #marshalls and unmarshalls the token
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

   #marshalls and unmarshalls the User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
