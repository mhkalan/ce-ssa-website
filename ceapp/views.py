from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializer import *
from .models import *

# Create your views here.


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
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
            serializer = self.serializer_class(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data='Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TAAPIView(generics.ListAPIView):
    serializer_class = TASerializer

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
