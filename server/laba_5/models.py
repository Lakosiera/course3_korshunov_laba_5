from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


# классы моделей (абстрактны структуры данных бля работы с базой данных)


# класс бля альбома
class Album(models.Model):
    # название альбома
    title = models.CharField(
        verbose_name="Название",  # название столбца в админке
        max_length=50,  # максимальная длина текста
        help_text="Название альбома",
    )
    # дата выпуска
    relesased_at = models.DateField(
        verbose_name="Дата выпуска",  # название столбца в админке
        help_text="Дата выпуска альбома",
    )
    # количесво трэков
    tracks = models.IntegerField(
        verbose_name="Кол-во треков",  # название столбца в админке
        validators=[
            # валидатор занчения, в данном случае минимальнео занчение должно быть равно 1
            MinValueValidator(
                1,  # минимальное значение
                # свое сообщение ошибки
                _("Значение должно быть больше или равно %(limit_value)s."),
            ),
        ],
        help_text="Кол-во треков в альбоме",
    )
    # артист
    artist = models.CharField(
        verbose_name="Артист",  # название столбца в админке
        max_length=50,  # максимальная длина текста
        blank=True,  # поле может быть пустым
        help_text="Артист",
    )
    # жанр
    genre = models.CharField(
        verbose_name="Жанр",  # название столбца в админке
        max_length=50,  # максимальная длина текста
        blank=True,  # поле может быть пустым
        help_text="Жанр",
    )
    # тип альбома (Studio / Live / Solo)
    type = models.CharField(
        verbose_name="Тип альбома",  # название столбца в админке
        max_length=50,  # максимальная длина текста
        blank=True,  # поле может быть пустым
        help_text="Тип альбома Дэмо / Дебютный / Промо / и т.д.",
    )
