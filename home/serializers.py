from rest_framework import serializers
from .models import Main_Model

class Main_serializer(serializers.ModelSerializer):
    class Meta:
        model = Main_Model
        # fields = "__all__"
        exclude = ['created_At','updated_At']

class Basic_Serializer(serializers.Serializer):
    pass


