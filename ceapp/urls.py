from django.urls import path, include
from .views import *


urlpatterns = [
    path('post/', PostAPIView.as_view(), name='post-view'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('ta/', TAAPIView.as_view(), name='ta-view'),
    path('report/', TAReportAPIView.as_view(), name='report-post'),
    path('admin-panel/login/', AdminPanelLoginAPIView.as_view(), name='admin-login'),
    path('admin-panel/post/', AdminPanelCreatePostAPIView.as_view(), name='admin-post'),
    path('admin-panel/ta/', AdminPanelCreateTAAPIView.as_view(), name='admin-ta'),
    path('admin-panel/post/<int:pk>/', AdminPanelPostDetailAPIView.as_view(), name='admin-post-detail'),
    path('admin-panel/ta/<int:pk>/', AdminPanelTADetailAPIView.as_view(), name='admin-ta-detail'),
    path('admin-panel/validate-token/', ValidateTokenAPIView.as_view(), name='validate-token'),
    path('admin-panel/delete-post/<int:pk>', DeletePostAPIView.as_view(), name='delete-post'),
]


