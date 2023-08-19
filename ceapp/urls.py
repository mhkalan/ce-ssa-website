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
    path('admin-panel/info/', AdminPanelInfoUpdateAPIView.as_view(), neme='admin-panel-info'),

    path('info/', InfoListAPIView.as_view(), name='info-list'),

    path('post/', PostAPIView.as_view(), name='post-view'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('post/top/', TopPostsAPIView.as_view(), name='top-post'),

    path('ta/', TAAPIView.as_view(), name='ta-view'),

    path('report/', TAReportAPIView.as_view(), name='report-post'),

    path('member/', MemberAPIView.as_view(), name='member-view'),

    path('ssa/', SSAListCreateView.as_view(), name='ssa-list'),

]
