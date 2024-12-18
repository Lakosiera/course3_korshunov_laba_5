from django import forms
from django.forms import ModelForm
from .models import Album


# класс для формы импорта файла
class ImportFileForm(forms.Form):
    # опциональное поле для нового имени файла
    filename = forms.CharField(
        max_length=50,  # максимальная длина текста
        required=False,  # необязательное поле
    )
    # поле для бинарных данных файла
    file = forms.FileField()
    # поле флаг (записывать ли в базу данных)
    to_db = forms.BooleanField(
        initial=False, # значение по умолчанию
        required=False,  # необязательное поле
    )


class NewAlbumForm(forms.Form):
    # поле для именем файла
    filename = forms.CharField(
        initial="albums", # значение по умолчанию
        required=False,  # необязательное поле
    )
    # поле флаг (записывать ли в базу данных)
    to_db = forms.BooleanField(
        initial=False, # значение по умолчанию
        required=False,  # необязательное поле
    )


class ActionForm(forms.Form):
    # поле для именем файла
    action = forms.CharField(
        required=True,  # обязательное поле
    )


# класс для формы данных музыкального альбома
# наследование от ModelForm позволяет подключить модель для работы с базой данных
class AlbumForm(ModelForm):
    class Meta:
        # чтобы указать что поле необязательное
        # в моделе надо указать 'blank=True'
        model = Album
        # fields = ["title", "relesased_at", "tracks", "artist", "genre", "type"] # только те поля которые нужны
        fields = "__all__"  # все поля
        exclude = ["id"]  # исключить поле


# Чтобы не дублировать одни и теже поля из модели Album
# Старый вариант формы больше не нужен
# # класс для формы данных музыкального альбома
# class MusicAlbumForm(forms.Form):
#     # название альбома
#     title = forms.CharField(
#         max_length=50,  # максимальная длина текста
#         required=True,  # обязательное поле
#     )
#     # дата выпуска
#     relesased_at = forms.DateField(
#         required=True,  # обязательное поле
#     )
#     # количесво трэков
#     length = forms.IntegerField(
#         min_value=1,  # минимальное значение
#         required=True,  # обязательное поле
#     )
#     # артист
#     artist = forms.CharField(
#         max_length=50,  # максимальная длина текста
#         required=False,  # необязательное поле
#     )
#     # жанр
#     genre = forms.CharField(
#         max_length=50,  # максимальная длина текста
#         required=False,  # необязательное поле
#     )
#     # тип альбома (Studio / Live / Solo)
#     type = forms.CharField(
#         max_length=50,  # максимальная длина текста
#         required=False,  # необязательное поле
#     )
