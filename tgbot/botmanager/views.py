from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render


from .models import TelegramUser
from bot.models import UserAction


def user_statistics(request):
    template = 'statistics.html'

    users_count = TelegramUser.objects.annotate(created_date=TruncDate('created_at')).values(
        'created_date').annotate(total=Count('id')).order_by('created_date')

    cumulative_total = 0
    for entry in users_count:
        cumulative_total += entry['total']
        entry['cumulative_total'] = cumulative_total

    user_actions = UserAction.objects.values('telegram_user__username').annotate(count_requests=Count('id'))

    datetime_actions = UserAction.objects.annotate(request_date=TruncDate('datetime')).values(
        'request_date').annotate(total=Count('id')).order_by('-request_date')

    all_requests = UserAction.objects.count()
    all_users = TelegramUser.objects.count()
    if all_users != 0:
        requests_for_user = round(all_requests / all_users, 2)
    else:
        requests_for_user = 0

    context: dict = {
        'users_count': users_count,
        'user_actions': user_actions,
        'datetime_actions': datetime_actions,
        'all_requests': all_requests,
        'all_users': all_users,
        'requests_for_user': requests_for_user

    }

    return render(request, template, context)
