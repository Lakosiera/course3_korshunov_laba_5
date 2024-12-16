from django.contrib import admin

from .models import Album


# класс обвертка над моделью 'Album' для работы в админке
class AlbumAdmin(admin.ModelAdmin):
    # отображаем поля обьекта в админке
    list_display = ('id', 'title', 'artist', 'relesased_at', 'length')


# регистрируем классы моделей бля работы с ними в админке
admin.site.register(Album, AlbumAdmin)
