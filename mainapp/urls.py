from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from .api_views import api_home, api_profile, api_other_profile, api_friends_list, api_workout_logs, api_achievements, \
    api_help_page

schema_view = get_schema_view(
    openapi.Info(
        title="Fitness Tracker API",
        default_version='v1',
        description="Track your fitness progress.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mezu4a@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=([permissions.IsAuthenticated]),
)

urlpatterns = [
    path('', views.home, name='home'),
    path("accounts/", include("allauth.urls")),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.other_profile, name='other_profile'),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friends/', views.friends_list, name='friends_list'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/register_workout/', views.register_workout, name='register_workout'),
    path('profile/set_goal', views.create_fitness_goal, name='create_fitness_goal'),
    path('profile/choose_goal', views.choose_goal, name='choose_goal'),
    path('profile/complete_goal', views.completed_goal, name='completed_goal'),
    path('profile/log_goal/<int:goal_id>/', views.log_goal_record, name='log_goal_record'),
    path('dashboard/', views.workout_logs, name='workout_logs'),
    path('create_activity/', views.create_activity, name='create_activity'),
    path('add_comment/<int:activity_id>', views.add_comment, name='add_comment'),
    path('like/<int:activity_id>/', views.like_activity, name='like_activity'),
    path('toggle-notification/', views.toggle_notification_setting, name='toggle_notification_setting'),
    path('achievements/', views.achievements, name='achievements'),
    path('help/', views.help_page, name='help_page'),
    path('submit_request/', views.submit_request, name='submit_request'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/home/', api_home, name='api_home'),
    path('api/profile/', api_profile, name='api_profile'),
    path('api/profile/<int:user_id>/', api_other_profile, name='api_other_profile'),
    path('api/friends/', api_friends_list, name='api_friends_list'),
    path('api/workout_logs/', api_workout_logs, name='api_workout_logs'),
    path('api/achievements/', api_achievements, name='api_achievements'),
    path('api/help/', api_help_page, name='api_help_page'),
]