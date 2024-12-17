from django.db import models

# классы моделей (абстрактны структуры данных бля работы с базой данных)


# класс бля альбома
class Album(models.Model):
    # поле индекса нужно для сохранения прогресса
    id = models.AutoField(
        primary_key=True,
        help_text="поле индекса записи",
    )
    # название альбома
    title = models.CharField(
        max_length=50,  # максимальная длина текста
        help_text="Название альбома",
    )
    # дата выпуска
    relesased_at = models.DateField(
        help_text="Дата выпуска альбома",
    )
    # количесво трэков
    length = models.IntegerField(
        help_text="Кол-во треков в альбоме",
    )
    # артист
    artist = models.CharField(
        max_length=50,  # максимальная длина текста
        help_text="Артист",
    )
    # жанр
    genre = models.CharField(
        max_length=50,  # максимальная длина текста
        help_text="Жанр",
    )
    # тип альбома (Studio / Live / Solo)
    type = models.CharField(
        max_length=50,  # максимальная длина текста
        help_text="Тип альбома Дэмо / Дебютный / Промо / и т.д.",
    )
