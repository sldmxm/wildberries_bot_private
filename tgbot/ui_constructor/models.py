from django.db import models


MAX_LENGTH_BUTTON_TEXT = 256
BUTTON_VERBOSE = 'Описание функционала кнопки'
UI_CONTROL_ID = 'ID редактируемого элемента'
DEFAULT_TEXT = 'Текст по умолчанию'
USERS_TEXT = 'Текст пользователя'


class ButtonConstructor(models.Model):
    """Модель конструктора кнопок."""

    ui_control_id = models.CharField(
        verbose_name=UI_CONTROL_ID,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    button_description = models.CharField(
        verbose_name=BUTTON_VERBOSE,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    default_text = models.CharField(
        verbose_name=DEFAULT_TEXT,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    users_text = models.CharField(
        verbose_name=USERS_TEXT,
        max_length=MAX_LENGTH_BUTTON_TEXT,
        blank=True,
    )

    class Meta:
        verbose_name = 'функционал'
        verbose_name_plural = 'Конструктор бота'

    def __str__(self):
        return self.ui_control_id
