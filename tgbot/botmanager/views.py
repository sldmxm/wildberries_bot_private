from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render


from .models import TelegramUser


def user_statistics(request):
    template = 'statistics.html'

    users_count = TelegramUser.objects.annotate(created_date=TruncDate('created_at')).values(
        'created_date').annotate(total=Count('id')).order_by('created_date')

    context: dict = {
        'users_count': users_count,
    }

    return render(request, template, context)
