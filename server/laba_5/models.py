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
    relesased_at = models.DateTimeField()
    # количесво трэков
    length = models.IntegerField()
    # артист
    artist = models.CharField(
        max_length=50,  # максимальная длина текста
    )
    # жанр
    genre = models.CharField(
        max_length=50,  # максимальная длина текста
    )
    # тип альбома (Studio / Live / Solo)
    type = models.CharField(
        max_length=50,  # максимальная длина текста
    )
