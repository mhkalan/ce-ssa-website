from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from ..serializer import *
from ..models import *


class AdminPanelLoginAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'msg': 'کاربر مورد نظر یافت نشد'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            if not user.is_superuser:
                return Response(
                    {
                        'status': status.HTTP_401_UNAUTHORIZED,
                        'msg': 'این کاربز ادمین نمیباشد'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
            }
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminPanelCreatePostAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminPanelCreateTAAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminPanelPostDetailAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "رویداد موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            post = Post.objects.get(pk=pk)
            serializer = self.get_serializer(post)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "رویداد موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AdminPanelCreatePostSerializer(request.data)
            title = serializer.data['title']
            description = serializer.data['description']
            image = request.FILES.get('image')
            post = Post.objects.get(pk=pk)
            post.title = title
            post.description = description
            post.image = image
            post.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminPanelTADetailAPIView(generics.ListCreateAPIView):
    serializer_class = TASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "حل تمرین موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            ta = TA.objects.get(pk=pk)
            serializer = self.get_serializer(ta)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "حل تمرین موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AdminPanelCreateTASerializer(request.data)
            name = serializer.data['name']
            subject = serializer.data['subject']
            teacher = serializer.data['teacher']
            ta = TA.objects.get(pk=pk)
            ta.name = name
            ta.subject = subject
            ta.teacher = teacher
            ta.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ValidateTokenAPIView(generics.CreateAPIView):
    serializer_class = ValidateTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        access_token = serializer.data['access_token']
        if not access_token:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    "msg": "شما نمیتوانید به عنوان ادمین وارد سایت شوید"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = AccessToken(access_token)
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_401_UNAUTHORIZED,
                    "msg": "شما از سایت خارج شدید دوباره وارد سایت شوید"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

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
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    "msg": "رویداد موردنظر یافت نشد",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                'msg': 'رویداد مورد نظر با موفقیت حذف شد'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class DeleteTaAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not TA.objects.filter(pk=pk).exists():
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    "msg": "حل تمرین موردنظر یافت نشد",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        ta = TA.objects.get(pk=pk)
        ta.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                'msg': 'حل تمرین مورد نظر با موفقیت حذف شد'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class AdminPanelCreateMemberAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            members = Member.objects.all()
            serializer = self.get_serializer(members, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
                return Response(
                    {
                        'status': status.HTTP_201_CREATED,
                        "msg": "عملیات موفقیت‌آمیز بود",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except:
                return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "msg": "متاسفانه سرور دچار اخنلال شده است",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class AdminPanelMemberDetailAPIView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "عضو موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            member = Member.objects.get(pk=pk)
            serializer = self.get_serializer(member)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "عضو موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AdminPanelCreateMemberSerializer(request.data)
            member = Member.objects.get(pk=pk)
            name = serializer.data['name']
            position = serializer.data['position']
            image = request.FILES.get('image')
            member.name = name
            member.position = position
            member.image = image
            member.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteMemberAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Member.objects.filter(pk=pk).exists():
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    "msg": "عضو موردنظر یافت نشد",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        member = Member.objects.get(pk=pk)
        member.delete()
        return Response(
            {
                "status": status.HTTP_204_NO_CONTENT,
                'msg': 'عضو مورد نظر با موفقیت حذف شد'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class AdminPanelListSSAAPIView(generics.ListAPIView):
    serializer_class = SSASerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            ssa = SSA.objects.all()
            serializer = self.get_serializer(ssa, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
                    return Response(
                        {
                            'status': status.HTTP_404_NOT_FOUND,
                            "msg": "عضو موردنظر یافت نشد",
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            for i in range(len(members)):
                member = Member.objects.get(pk=members[i])
                members_info.append(member)
            ssa_instance = SSA.objects.create(year=year)
            ssa_instance.members.set(members_info)
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminPanelInfoUpdateAPIView(generics.ListCreateAPIView):
    serializer_class = InfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            info = Info.objects.get(pk=1)
            serializer = self.get_serializer(info)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
                return Response(
                    {
                        'status': status.HTTP_201_CREATED,
                        "msg": "عملیات موفقیت‌آمیز بود",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            info = Info.objects.get(pk=1)
            serializer = AdminPanelInfoUpdateSerializer(request.data)
            about_us = serializer.data['aboutUs']
            rights = serializer.data['rights']
            homepage = serializer.data['homepage']
            info.aboutUs = about_us
            info.rights = rights
            info.homepage = homepage
            info.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سرور دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
