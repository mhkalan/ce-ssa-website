from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from ..serializer import *
from ..models import *


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDetailAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TopPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-id')[:3]
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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TAAPIView(generics.ListAPIView):
    serializer_class = TASerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            names = [item['name'] for item in serializer.data]
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    "msg": "عملیات موفقیت‌آمیز بود",
                    "data": names
                },
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TAReportAPIView(generics.CreateAPIView):
    serializer_class = TAReportSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            ta = serializer.data['ta_name']
            if not TA.objects.filter(name=ta).exists():
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        "msg": "حل تمرین موردنظر یافت نشد",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            ta_name = TA.objects.get(name=ta)
            text = serializer.data['text']
            TAReport.objects.create(
                TA=ta_name,
                text=text
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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MemberAPIView(generics.ListAPIView):
    serializer_class = MemberSerializer

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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SSAListCreateView(generics.ListAPIView):
    serializer_class = SSASerializer

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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfoListAPIView(generics.ListAPIView):
    serializer_class = InfoSerializer

    def get(self, request, *args, **kwargs):
        try:
            info = Info.objects.all()
            serializer = self.get_serializer(info, many=True)
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
                    "msg": "متاسفانه سزوز دچار اخنلال شده است",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

