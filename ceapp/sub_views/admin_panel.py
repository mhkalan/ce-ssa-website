from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from ..serializer import *
from ..models import *
from ..utills import *


class AdminPanelLoginAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return status404response()
            if not user.is_superuser:
                return status401response()
            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
            }
            return status200response(data)
        except:
            return status500response()


class AdminPanelCreatePostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            author = request.user
            serializer = AdminPanelCreatePostSerializer(request.data)
            title = serializer.data['title']
            description = serializer.data['description']
            image = request.FILES.get('image')
            Post.objects.create(
                author=author,
                title=title,
                description=description,
                image=image
            )
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelCreateTAAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            serializer = AdminPanelCreateTASerializer(request.data)
            name = serializer.data['name']
            subject = serializer.data['subject']
            teacher = serializer.data['teacher']
            TA.objects.create(
                name=name,
                subject=subject,
                teacher=teacher
            )
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelPostDetailAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return status404response()
            post = Post.objects.get(pk=pk)
            serializer = self.get_serializer(post)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return status404response()
            serializer = AdminPanelCreatePostSerializer(request.data)
            title = serializer.data['title']
            description = serializer.data['description']
            image = request.FILES.get('image')
            post = Post.objects.get(pk=pk)
            post.title = title
            post.description = description
            post.image = image
            post.save()
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelTADetailAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return status404response()
            ta = TA.objects.get(pk=pk)
            serializer = self.get_serializer(ta)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return status404response()
            serializer = AdminPanelCreateTASerializer(request.data)
            name = serializer.data['name']
            subject = serializer.data['subject']
            teacher = serializer.data['teacher']
            ta = TA.objects.get(pk=pk)
            ta.name = name
            ta.subject = subject
            ta.teacher = teacher
            ta.save()
            return status201response(serializer.data)
        except:
            return status500response()


class ValidateTokenAPIView(generics.CreateAPIView):
    serializer_class = ValidateTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        access_token = serializer.data['access_token']
        if not access_token:
            return status400response()
        try:
            token = AccessToken(access_token)
        except Exception as e:
            return status401response()

        return Response(
            {
                'ststus': status.HTTP_200_OK,
                "msg": "Token is valid",
            },
            status=status.HTTP_200_OK
        )


class DeletePostAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Post.objects.filter(pk=pk).exists():
            return status404response()
        post = Post.objects.get(pk=pk)
        post.delete()
        return status204response()


class DeleteTaAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not TA.objects.filter(pk=pk).exists():
            return status404response()
        ta = TA.objects.get(pk=pk)
        ta.delete()
        return status204response()


class AdminPanelCreateMemberAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            members = Member.objects.all()
            serializer = self.get_serializer(members, many=True)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            serializer = AdminPanelCreateMemberSerializer(request.data)
            name = serializer.data['name']
            position = serializer.data['position']
            image = request.FILES.get('image')
            Member.objects.create(
                name=name,
                position=position,
                image=image
            )
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelMemberDetailAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return status404response()
            member = Member.objects.get(pk=pk)
            serializer = self.get_serializer(member)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return status404response()
            serializer = AdminPanelCreateMemberSerializer(request.data)
            member = Member.objects.get(pk=pk)
            name = serializer.data['name']
            position = serializer.data['position']
            image = request.FILES.get('image')
            member.name = name
            member.position = position
            member.image = image
            member.save()
            return status201response(serializer.data)
        except:
            return status500response()


class DeleteMemberAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Member.objects.filter(pk=pk).exists():
            return status404response()
        member = Member.objects.get(pk=pk)
        member.delete()
        return status204response()


class AdminPanelListSSAAPIView(generics.ListAPIView):
    serializer_class = SSASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ssa = SSA.objects.all()
            serializer = self.get_serializer(ssa, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelCreateSSAAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateSSASerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            year = serializer.data['year']
            members = serializer.data['members']
            members_info = []
            for i in range(len(members)):
                if not Member.objects.filter(pk=members[i]).exists():
                    return status404response()
            for i in range(len(members)):
                member = Member.objects.get(pk=members[i])
                members_info.append(member)
            ssa_instance = SSA.objects.create(year=year)
            ssa_instance.members.set(members_info)
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelSSADetailAPIView(generics.ListAPIView):
    serializer_class = SSASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not SSA.objects.filter(pk=pk).exists():
                return status404response()
            ssa = SSA.objects.get(pk=pk)
            serializer = self.get_serializer(ssa)
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelUpdateSSAAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateSSASerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not SSA.objects.filter(pk=pk).exists():
                return status404response()
            ssa = SSA.objects.get(pk=pk)
            serializer = self.get_serializer(request.data)
            year = serializer.data['year']
            members = serializer.data['members']
            members_info = []
            for i in range(len(members)):
                if not Member.objects.filter(pk=members[i]).exists():
                    return status404response()
            for i in range(len(members)):
                member = Member.objects.get(pk=members[i])
                members_info.append(member)
            ssa.year = year
            ssa.members.set(members_info)
            ssa.save()
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelInfoUpdateAPIView(generics.ListCreateAPIView):
    serializer_class = InfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            info = Info.objects.get(pk=1)
            serializer = self.get_serializer(info)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            if not Info.objects.filter(pk=1).exists():
                serializer = AdminPanelInfoUpdateSerializer(request.data)
                about_us = serializer.data['aboutUs']
                rights = serializer.data['rights']
                homepage = serializer.data['homepage']
                Info.objects.create(
                    aboutUs=about_us,
                    rights=rights,
                    homepage=homepage
                )
                return status201response(serializer.data)
            info = Info.objects.get(pk=1)
            serializer = AdminPanelInfoUpdateSerializer(request.data)
            about_us = serializer.data['aboutUs']
            rights = serializer.data['rights']
            homepage = serializer.data['homepage']
            info.aboutUs = about_us
            info.rights = rights
            info.homepage = homepage
            info.save()
            return status201response(serializer.data)
        except:
            return status500response()
