from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):

    def get_author(self, obj):
        return obj.author.username

    author = serializers.SerializerMethodField('get_author', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class TASerializer(serializers.ModelSerializer):

    class Meta:
        model = TA
        fields = '__all__'


class TAReportSerializer(serializers.Serializer):
    ta_name = serializers.CharField()
    text = serializers.CharField()

