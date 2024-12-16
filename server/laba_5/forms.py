from django import forms


# класс для формы импорта файла
class ImportFileForm(forms.Form):
    # опциональное поле для нового имени файла
    filename = forms.CharField(
        max_length=50, # максимальная длина текста
        required=False, # необязательное поле
    )
    # поле для бинарных данных файла
    file = forms.FileField()


# класс для формы данных музыкального альбома
class MusicAlbumForm(forms.Form):
    # название альбома
    title = forms.CharField(
        max_length=50, # максимальная длина текста
        required=True, # обязательное поле
    )
    # дата выпуска
    relesased_at = forms.CharField(
        max_length=50, # максимальная длина текста
        required=True, # обязательное поле
    )
    # количесво трэков
    length = forms.IntegerField(
        min_value=1, # минимальное значение
        required=True, # обязательное поле
    )
    # артист
    artist = forms.CharField(
        max_length=50, # максимальная длина текста
        required=False, # необязательное поле
    )
    # жанр
    genre = forms.CharField(
        max_length=50, # максимальная длина текста
        required=False, # необязательное поле
    )
    # тип альбома (Studio / Live / Solo)
    type = forms.CharField(
        max_length=50, # максимальная длина текста
        required=False, # необязательное поле
    )
