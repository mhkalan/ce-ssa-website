from django.urls import path, include
from .views import *


urlpatterns = [
    path('post/', PostAPIView.as_view(), name='post-view'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('ta/', TAAPIView.as_view(), name='ta-view'),
    path('report/', TAReportAPIView.as_view(), name='report-post'),
]
