from django.db import models

from bot.constants import actions
from botmanager.models import TelegramUser


USER_ACTIONS = (
    (actions.POSITION_PARSER, actions.POSITION_PARSER),
    (actions.UPDATE_POSITION, actions.UPDATE_POSITION),
    (actions.RESIDUE_PARSER, actions.RESIDUE_PARSER),
    (actions.ACCEPTANCE_RATE, actions.ACCEPTANCE_RATE),
    (actions.USER_SUBSCRIPTIONS, actions.USER_SUBSCRIPTIONS),
    (actions.SUBSCRIBE, actions.SUBSCRIBE),
    (actions.UNSUBSCRIBE, actions.UNSUBSCRIBE),
    (actions.EXPORT_RESULTS, actions.EXPORT_RESULTS),
)


class Callback(models.Model):
    query = models.TextField(blank=False, null=False)
    article = models.IntegerField(null=False)
    interval = models.DurationField(null=True)
    start_time = models.DateTimeField(null=True)


class UserAction(models.Model):
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=USER_ACTIONS)
