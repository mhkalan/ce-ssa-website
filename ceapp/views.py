from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from .serializer import *
from .models import *


# Create your views here.


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return Response(data='No Content', status=status.HTTP_404_NOT_FOUND)
            post = Post.objects.get(pk=pk)
            serializer = self.get_serializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-id')[:3]
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TAAPIView(generics.ListAPIView):
    serializer_class = TASerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            names = [item['name'] for item in serializer.data]
            return Response(data=names, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TAReportAPIView(generics.CreateAPIView):
    serializer_class = TAReportSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            ta = serializer.data['ta_name']
            if not TA.objects.filter(name=ta).exists():
                return Response(data='No TA Found', status=status.HTTP_404_NOT_FOUND)
            ta_name = TA.objects.get(name=ta)
            text = serializer.data['text']
            TAReport.objects.create(
                TA=ta_name,
                text=text
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelLoginAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response(data='این نام کاربری و رمز معتبر نمی باشد')
            if not user.is_superuser:
                return Response(data='این کاربر ادمین نمی باشد')
            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
            }
            return Response(data=data)
        except:
            return Response(data='خطای سرور')


class AdminPanelCreatePostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            author = request.user
            serializer = AdminPanelCreatePostSerializer(request.data)
            title = serializer.data['title']
            description = serializer.data['description']
            Post.objects.create(
                author=author,
                title=title,
                description=description,
            )
            return Response(data=serializer.data)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelCreateTAAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response(data=serializer.data)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelPostDetailAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return Response(data='No Content', status=status.HTTP_404_NOT_FOUND)
            post = Post.objects.get(pk=pk)
            serializer = self.get_serializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return Response(data='No Content', status=status.HTTP_404_NOT_FOUND)
            serializer = AdminPanelCreatePostSerializer(request.data)
            title = serializer.data['title']
            description = serializer.data['description']
            post = Post.objects.get(pk=pk)
            post.title = title
            post.description = description
            post.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelTADetailAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return Response(data='No Content', status=status.HTTP_404_NOT_FOUND)
            ta = TA.objects.get(pk=pk)
            serializer = self.get_serializer(ta)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return Response(data='No Content', status=status.HTTP_404_NOT_FOUND)
            serializer = AdminPanelCreateTASerializer(request.data)
            name = serializer.data['name']
            subject = serializer.data['subject']
            teacher = serializer.data['teacher']
            ta = TA.objects.get(pk=pk)
            ta.name = name
            ta.subject = subject
            ta.teacher = teacher
            ta.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidateTokenAPIView(generics.CreateAPIView):
    serializer_class = ValidateTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        access_token = serializer.data['access_token']

        if not access_token:
            return Response({"error": "Access token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(access_token)
            token_payload = token.payload
        except Exception as e:
            return Response({"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Token is valid.", "user_id": token_payload.get('user_id')})


class DeletePostAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Post.objects.filter(pk=pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteTaAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not TA.objects.filter(pk=pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        ta = TA.objects.get(pk=pk)
        ta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberAPIView(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        try:
            members = Member.objects.all()
            serializer = self.get_serializer(members, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelCreateMemberAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            members = Member.objects.all()
            serializer = self.get_serializer(members, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AdminPanelCreateMemberSerializer(request.data)
            name = serializer.data['name']
            position = serializer.data['position']
            image = serializer.data['image']
            Member.objects.create(
                name=name,
                position=position,
                image=image
            )
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelMemberDetailAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            member = Member.objects.get(pk=pk)
            serializer = self.get_serializer(member)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = AdminPanelCreateMemberSerializer(request.data)
            member = Member.objects.get(pk=pk)
            name = serializer.data['name']
            position = serializer.data['position']
            image = serializer.data['image']
            member.name = name
            member.position = position
            member.image = image
            member.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteMemberAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Member.objects.filter(pk=pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        member = Member.objects.get(pk=pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SSAListCreateView(generics.ListAPIView):
    serializer_class = SSASerializer

    def get(self, request, *args, **kwargs):
        try:
            ssa = SSA.objects.all()
            serializer = self.get_serializer(ssa, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPanelListSSAAPIView(generics.ListAPIView):
    serializer_class = SSASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ssa = SSA.objects.all()
            serializer = self.get_serializer(ssa, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                member = Member.objects.get(pk=members[i])
                members_info.append(member)
            ssa_instance = SSA.objects.create(year=year)
            ssa_instance.members.set(members_info)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
