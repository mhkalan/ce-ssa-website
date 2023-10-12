from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from ..serializer import *
from ..models import *
from ..utills import *

User = get_user_model()


class AdminInformationAPIView(generics.ListAPIView):
    serializer_class = SuperuserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user_information = User.objects.get(username=user)
            serializer = self.get_serializer(user_information)
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelLoginAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return status404response(msg='چنین کاربری وجود ندارد')
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
            date = serializer.data['date']
            image = request.FILES.get('image')
            Post.objects.create(
                author=author,
                title=title,
                description=description,
                date=date,
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
            TA.objects.create(
                name=name,
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
                return status404response(msg='رویداد مورد نظر یافت نشد')
            post = Post.objects.get(pk=pk)
            serializer = self.get_serializer(post)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Post.objects.filter(pk=pk).exists():
                return status404response(msg='رویداد مورد نظر یافت نشد')
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
                return status404response(msg='حل تمرین مورد نظر یافت نشد')
            ta = TA.objects.get(pk=pk)
            serializer = self.get_serializer(ta)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not TA.objects.filter(pk=pk).exists():
                return status404response(msg='حل تمرین مورد نظر یافت نشد')
            serializer = AdminPanelCreateTASerializer(request.data)
            name = serializer.data['name']
            ta = TA.objects.get(pk=pk)
            ta.name = name
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
            return status404response(msg='رویداد مورد نظر یافت نشد')
        post = Post.objects.get(pk=pk)
        post.delete()
        return status204response()


class DeleteTaAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not TA.objects.filter(pk=pk).exists():
            return status404response(msg='حل تمرین مورد نظر یافت نشد')
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
                return status404response(msg='عضو مورد نظر یافت نشد')
            member = Member.objects.get(pk=pk)
            serializer = self.get_serializer(member)
            return status200response(serializer.data)
        except:
            return status500response()

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Member.objects.filter(pk=pk).exists():
                return status404response(msg='عضو مورد نظر یافت نشد')
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
            return status404response(msg='عضو مورد نظر یافت نشد')
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
            # members = serializer.data['members']
            # members_info = []
            # for i in range(len(members)):
            #     if not Member.objects.filter(pk=members[i]).exists():
            #         return status404response(msg='عضو مورد نظر یافت نشد')
            # for i in range(len(members)):
            #     member = Member.objects.get(pk=members[i])
            #     members_info.append(member)
            SSA.objects.create(year=year)
            # ssa_instance.members.set(members_info)
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
                return status404response(msg='انجمن مورد نظر یافت نشد')
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
                return status404response(msg='انجمن مورد نظر یافت نشد')
            ssa = SSA.objects.get(pk=pk)
            serializer = self.get_serializer(request.data)
            year = serializer.data['year']
            # members = serializer.data['members']
            # members_info = []
            # for i in range(len(members)):
            #     if not Member.objects.filter(pk=members[i]).exists():
            #         return status404response(msg='عضو مورد نظر یافت نشد')
            # for i in range(len(members)):
            #     member = Member.objects.get(pk=members[i])
            #     members_info.append(member)
            ssa.year = year
            # ssa.members.set(members_info)
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


class AdminPanelClassListAPIView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            class_info = Class.objects.all()
            serializer = self.get_serializer(class_info, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelCreateClassAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateClassSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            name = serializer.data['name']
            group_number = serializer.data['group_number']
            teacher_name = serializer.data['teacher_name']
            class_time = serializer.data['class_time']
            ta_class = serializer.data['ta_class']
            channel_link = serializer.data['channel_link']
            ta = serializer.data['ta']
            image = request.FILES.get('image')
            ta_info = []
            for i in range(len(ta)):
                if not TA.objects.filter(pk=ta[i]).exists():
                    return status404response(msg='حل تمرین مورد نظر یافت نشد')
            for i in range(len(ta)):
                person = TA.objects.get(pk=ta[i])
                ta_info.append(person)
            class_instance = Class.objects.create(
                name=name,
                group_number=group_number,
                teacher_name=teacher_name,
                class_time=class_time,
                ta_class=ta_class,
                channel_link=channel_link,
                image=image
            )
            class_instance.ta.set(ta_info)
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelClassDetailAPIView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Class.objects.filter(pk=pk).exists():
                return status404response(msg='درس مورد نظر یافت نشد')
            class_info = Class.objects.get(pk=pk)
            serializer = self.get_serializer(class_info)
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelUpdateClassAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateClassSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not Class.objects.filter(pk=pk).exists():
                return status404response(msg='درس مورد نظر یافت نشد')
            class_info = Class.objects.get(pk=pk)
            serializer = self.get_serializer(request.data)
            name = serializer.data['name']
            group_number = serializer.data['group_number']
            teacher_name = serializer.data['teacher_name']
            class_time = serializer.data['class_time']
            ta_class = serializer.data['ta_class']
            channel_link = serializer.data['channel_link']
            ta = serializer.data['ta']
            image = request.FILES.get('image')
            ta_info = []
            for i in range(len(ta)):
                if not TA.objects.filter(pk=ta[i]).exists():
                    return status404response(msg='حل تمرین مورد نظر یافت نشد')
            for i in range(len(ta)):
                person = TA.objects.get(pk=ta[i])
                ta_info.append(person)
            class_info.name = name
            class_info.group_number = group_number
            class_info.teacher_name = teacher_name
            class_info.class_time = class_time
            class_info.ta_class = ta_class
            class_info.channel_link = channel_link
            class_info.image = image
            class_info.ta.set(ta_info)
            class_info.save()
            return status201response(serializer.data)
        except:
            return status500response()


class DeleteSSAAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not SSA.objects.filter(pk=pk).exists():
            return status404response(msg='انجمن مورد نظر یافت نشد')
        ssa = SSA.objects.get(pk=pk)
        ssa.delete()
        return status204response()


class DeleteClassAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not Class.objects.filter(pk=pk).exists():
            return status404response(msg='درس مورد نظر یافت نشد')
        class_instance = Class.objects.get(pk=pk)
        class_instance.delete()
        return status204response()


class AdminPanelGetTAReportAPIView(generics.ListAPIView):
    serializer_class = TAReportGetSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            reports = TAReport.objects.all()
            serializer = self.get_serializer(reports, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class AdminPanelGetTAReportByNameAPIView(generics.ListAPIView):
    serializer_class = TAReportGetSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            name = kwargs.get('name')
            if not TAReport.objects.filter(TA__name=name).exists():
                return status404response('حل تمرین مورد نظر یافت نشد')
            reports = TAReport.objects.filter(TA__name=name)
            serializer = self.get_serializer(reports, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class DeleteTAReportAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not TAReport.objects.filter(pk=pk).exists():
            return status404response('گزارش مورد نظر یافت نشد')
        report = TAReport.objects.get(pk=pk)
        report.delete()
        return status204response()


class AdminPanelAddMemberToSSAAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateMemberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            if not SSA.objects.filter(pk=pk).exists():
                return status404response('انجمن مورد نظر یافت نشد')
            ssa_instance = SSA.objects.get(pk=pk)
            serializer = self.get_serializer(request.data)
            name = serializer.data['name']
            position = serializer.data['position']
            image = request.FILES.get('image')
            Member.objects.create(
                name=name,
                position=position,
                image=image
            )
            member = Member.objects.all().order_by('-id')[0]
            member_info = [member]
            ssa_instance.members.add(*member_info)
            return status201response(serializer.data)
        except:
            return status500response()


class AdminPanelDeleteMemberFromSSAAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            ssa_pk = kwargs.get('ssa')
            member_pk = kwargs.get('member')
            if not SSA.objects.filter(pk=ssa_pk).exists():
                return status404response('انجمن مورد نظر یافت نشد')
            if not Member.objects.filter(pk=member_pk).exists():
                return status404response('عضو مورد نظر یافت نشد')
            member_instance = Member.objects.get(pk=member_pk)
            ssa_instance = SSA.objects.get(pk=ssa_pk)
            ssa_instance.members.remove(member_instance)
            return status204response()
        except:
            return status500response()


class AdminPanelEditMemberSSAAPIView(generics.CreateAPIView):
    serializer_class = AdminPanelCreateMemberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            ssa_pk = kwargs.get('ssa')
            member_pk = kwargs.get('member')
            if not SSA.objects.filter(pk=ssa_pk).exists():
                return status404response('انجمن مورد نظر یافت نشد')
            if not Member.objects.filter(pk=member_pk).exists():
                return status404response('عضو مورد نظر یافت نشد')
            member_instance = None
            ssa_instance = SSA.objects.get(pk=ssa_pk)
            serializer = self.get_serializer(request.data)
            name = serializer.data['name']
            position = serializer.data['position']
            image = request.FILES.get('image')
            for member in ssa_instance.members.all():
                if member.pk == member_pk:
                    member_instance = member
                    ssa_instance.members.remove(member)
            member_instance.name = name
            member_instance.position = position
            member_instance.image = image
            member_instance.save()
            member_info = [member_instance]
            ssa_instance.members.add(*member_info)
            return status200response(serializer.data)
        except:
            return status500response()

