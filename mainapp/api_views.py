from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Activity, CompletedGoals, Workout, Badge
from .models import Friendship


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_home(request):
    activities = Activity.objects.order_by('-pub_date')[:5].values()
    return JsonResponse(list(activities), safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    user = request.user
    completed_goals_count = CompletedGoals.objects.filter(user=user).count()
    activities_count = Activity.objects.filter(user=user).count()
    workouts_count = Workout.objects.filter(user=user).count()
    badges = Badge.objects.filter(user=user).values('badge_type').annotate(count=Count('id'))
    context = {
        'username': user.username,
        'completed_goals_count': completed_goals_count,
        'activities_count': activities_count,
        'workouts_count': workouts_count,
        'badges': list(badges)
    }
    return JsonResponse(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_other_profile(request, user_id):
    if user_id == request.user.id:
        return redirect('api_profile')

    user = get_object_or_404(User, id=user_id)
    completed_goals_count = CompletedGoals.objects.filter(user=user).count()
    activities_count = Activity.objects.filter(user=user).count()
    workouts_count = Workout.objects.filter(user=user).count()
    badges = Badge.objects.filter(user=user).values('badge_type').annotate(count=Count('id'))

    context = {
        'username': user.username,
        'completed_goals_count': completed_goals_count,
        'activities_count': activities_count,
        'workouts_count': workouts_count,
        'badges': list(badges)
    }
    return JsonResponse(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_friends_list(request):
    friends = Friendship.objects.filter(user=request.user).values('friend__username', 'friend__id')
    return JsonResponse(list(friends), safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_workout_logs(request):
    total_logs = Workout.objects.filter(user=request.user).order_by('-date').all().values()

    total_workouts = len(total_logs)
    total_all_sets_done = sum(1 for log in total_logs if log['all_sets_done'])
    total_all_arms_done = sum(1 for log in total_logs if log['all_arms_done'])
    total_all_legs_done = sum(1 for log in total_logs if log['all_legs_done'])
    total_all_chest_done = sum(1 for log in total_logs if log['all_chest_done'])

    # Calculate percentages
    percentage_all_sets_done = (total_all_sets_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_arms_done = (total_all_arms_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_legs_done = (total_all_legs_done / total_workouts) * 100 if total_workouts > 0 else 0
    percentage_all_chest_done = (total_all_chest_done / total_workouts) * 100 if total_workouts > 0 else 0

    recent_logs = total_logs[:5]
    completed_goals = CompletedGoals.objects.filter(user=request.user)[:5].values()

    return JsonResponse({
        'logs': list(recent_logs),
        'percentage_all_sets_done': percentage_all_sets_done,
        'percentage_all_arms_done': percentage_all_arms_done,
        'percentage_all_legs_done': percentage_all_legs_done,
        'percentage_all_chest_done': percentage_all_chest_done,
        'completed_goals': list(completed_goals),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_achievements(request):
    workout_badge = Badge.objects.filter(user=request.user, awarded_for='Workout').values('badge_type').annotate(
        count=Count('badge_type'))
    goal_badge = Badge.objects.filter(user=request.user, awarded_for='Goal').values('badge_type').annotate(
        count=Count('badge_type'))
    post_badge = Badge.objects.filter(user=request.user, awarded_for='Post').values('badge_type').annotate(
        count=Count('badge_type'))
    comments_badge = Badge.objects.filter(user=request.user, awarded_for='Comment').values('badge_type').annotate(
        count=Count('badge_type'))

    return JsonResponse({
        'workout_badge': list(workout_badge),
        'goal_badge': list(goal_badge),
        'post_badge': list(post_badge),
        'comments_badge': list(comments_badge),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_help_page(request):
    return JsonResponse({'help': 'This is the help page content.'})
