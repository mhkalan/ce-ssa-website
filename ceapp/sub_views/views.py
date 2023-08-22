from rest_framework import generics
from rest_framework.permissions import AllowAny


from ..serializer import *
from ..models import *
from ..utills import *


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return status200response(serializer.data)
        except:
            return status500response()


class PostDetailAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

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


class TopPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-id')[:3]
            serializer = self.get_serializer(posts, many=True)
            for post_data in serializer.data:
                post_data['image'] = request.build_absolute_uri(post_data['image'])
            return status200response(serializer.data)
        except:
            return status500response()


class TAAPIView(generics.ListAPIView):
    serializer_class = TASerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            ta = TA.objects.all()
            serializer = self.get_serializer(ta, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class TAReportAPIView(generics.CreateAPIView):
    serializer_class = TAReportSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(request.data)
            ta = serializer.data['ta_name']
            if not TA.objects.filter(name=ta).exists():
                return status404response()
            ta_name = TA.objects.get(name=ta)
            text = serializer.data['text']
            TAReport.objects.create(
                TA=ta_name,
                text=text
            )
            return status201response(serializer.data)
        except:
            return status500response()


class MemberAPIView(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        try:
            members = Member.objects.all()
            serializer = self.get_serializer(members, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class SSAListCreateView(generics.ListAPIView):
    serializer_class = SSASerializer

    def get(self, request, *args, **kwargs):
        try:
            ssa = SSA.objects.all()
            serializer = self.get_serializer(ssa, many=True)
            return status200response(serializer.data)
        except:
            return status500response()


class InfoListAPIView(generics.ListAPIView):
    serializer_class = InfoSerializer

    def get(self, request, *args, **kwargs):
        try:
            info = Info.objects.get(pk=1)
            serializer = self.get_serializer(info)
            return status200response(serializer.data)
        except:
            return status500response()
