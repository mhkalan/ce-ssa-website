from django.urls import path
from .sub_views.admin_panel import *
from .sub_views.views import *


urlpatterns = [
    path('admin-panel/login/', AdminPanelLoginAPIView.as_view(), name='admin-login'),
    path('admin-panel/validate-token/', ValidateTokenAPIView.as_view(), name='validate-token'),
    path('admin-panel/post/', AdminPanelCreatePostAPIView.as_view(), name='admin-post'),
    path('admin-panel/post/<int:pk>/', AdminPanelPostDetailAPIView.as_view(), name='admin-post-detail'),
    path('admin-panel/delete-post/<int:pk>', DeletePostAPIView.as_view(), name='delete-post'),
    path('admin-panel/ta/', AdminPanelCreateTAAPIView.as_view(), name='admin-ta'),
    path('admin-panel/ta/<int:pk>/', AdminPanelTADetailAPIView.as_view(), name='admin-ta-detail'),
    path('admin-panel/delete-ta/<int:pk>', DeleteTaAPIView.as_view(), name='delete-ta'),
    path('admin-panel/member/', AdminPanelCreateMemberAPIView.as_view(), name='admin-member'),
    path('admin-panel/member/<int:pk>/', AdminPanelMemberDetailAPIView.as_view(), name='admin-member-detail'),
    path('admin-panel/delete-member/<int:pk>/', DeleteMemberAPIView.as_view(), name='delete-member'),
    path('admin-panel/ssa/list/', AdminPanelListSSAAPIView.as_view(), name='admin-ssa-list'),
    path('admin-panel/ssa/create/', AdminPanelCreateSSAAPIView.as_view(), name='admin-ssa-create'),
    path('admin-panel/ssa/detail/<int:pk>/', AdminPanelSSADetailAPIView.as_view(), name='admin-ssa-detail'),
    path('admin-panel/ssa/update/<int:pk>/', AdminPanelUpdateSSAAPIView.as_view(), name='admin-ssa-update'),
    path('admin-panel/ssa/delete/<int:pk>/', DeleteSSAAPIView.as_view(), name='delete-ssa'),
    path('admin-panel/class/list/', AdminPanelClassListAPIView.as_view(), name='admin-class-list'),
    path('admin-panel/class/create/', AdminPanelCreateClassAPIView.as_view(), name='admin-class-create'),
    path('admin-panel/class/detail/<int:pk>/', AdminPanelClassDetailAPIView.as_view(), name='admin-class-detail'),
    path('admin-panel/class/update/<int:pk>/', AdminPanelUpdateClassAPIView.as_view(), name='admin-class-update'),
    path('admin-panel/class/delete/<int:pk>/', DeleteClassAPIView.as_view(), name='delete-class'),
    path('admin-panel/info/', AdminPanelInfoUpdateAPIView.as_view(), name='admin-panel-info'),
    path('admin-panel/report/', AdminPanelGetTAReportAPIView.as_view(), name='admin-panel-report'),
    path('admin-panel/report/<str:name>/', AdminPanelGetTAReportByNameAPIView.as_view(),
         name='admin-panel-report-name'),
    path('admin-panel/report/delete/<int:pk>/', DeleteTAReportAPIView.as_view(), name='delete-report'),

    path('info/', InfoListAPIView.as_view(), name='info-list'),

    path('post/', PostAPIView.as_view(), name='post-view'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('post/top/', TopPostsAPIView.as_view(), name='top-post'),
    path('ta/', TAAPIView.as_view(), name='ta-view'),

    path('report/', TAReportAPIView.as_view(), name='report-post'),

    path('member/', MemberAPIView.as_view(), name='member-view'),

    path('ssa/', SSAListView.as_view(), name='ssa-list'),

    path('class/', ClassListAPIView.as_view(), name='class-list'),
    path('class/<int:pk>/', ClassDetailAPIView.as_view(), name='class-detail'),
]
