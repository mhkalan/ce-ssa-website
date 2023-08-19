from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):

    def get_author(self, obj):
        return obj.author.username

    author = serializers.SerializerMethodField('get_author', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['created_at']


class TASerializer(serializers.ModelSerializer):

    class Meta:
        model = TA
        fields = '__all__'


class TAReportSerializer(serializers.Serializer):
    ta_name = serializers.CharField()
    text = serializers.CharField()


class AdminPanelLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AdminPanelCreatePostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class AdminPanelCreateTASerializer(serializers.Serializer):
    name = serializers.CharField()
    subject = serializers.CharField()
    teacher = serializers.CharField()


class ValidateTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'


class AdminPanelCreateMemberSerializer(serializers.Serializer):
    name = serializers.CharField()
    position = serializers.CharField()
    image = serializers.CharField()


class SSASerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = SSA
        fields = '__all__'


class ListMembersField(serializers.ListField):
    child = serializers.IntegerField()


class AdminPanelCreateSSASerializer(serializers.Serializer):
    year = serializers.IntegerField()
    members = ListMembersField()


class InfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Info
        fields = '__all__'


class AdminPanelInfoUpdateSerializer(serializers.Serializer):
    aboutUs = serializers.CharField()
    rights = serializers.CharField()
    homepage = serializers.CharField()

