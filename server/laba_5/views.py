import string
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib import messages
import json
from datetime import datetime
from .models import Album
from .forms import ActionForm, AlbumForm, ImportFileForm, NewAlbumForm
from .file_utils import (
    write_json,
    write_file,
    read_file,
    read_dir,
    delete_file,
    json_str,
    read_json,
)

# имя куки для хранения номера вкладки
COOKIE_ACTIVE_TAB = "laba_5_tab"


# пример простейшей вьющки
def hello_world(request):
    # простейший вывод html страницы
    return HttpResponse("Hello, world!")


# вьбшка главной страници
def index(request):
    # читаем список всех файло бля отображения во вкладке экспорт
    files = read_dir()
    # получаем из куки на какой вкладке мы были
    tab_index = request.COOKIES.get(COOKIE_ACTIVE_TAB, "0")
    # передаем данные контекста
    context = {
        # параметр заголовока
        "name": "Laba 5 - Музыкальные альбомы",
        # список файлов
        "files": files,
        # интекс вкладки
        "tab_index": tab_index,
        # все данные из базы данных
        "albums": Album.objects.all(),
    }
    # ренедр вьюшки в html страницу
    return render(request, "index.html", context)


# вьюшка для создания альбома
# она не отображает свою страницу а перенаправляет на главную
def add_album(request):
    # проверяем что медод запроса "POST"
    if request.method == "POST":
        # получаем данные формы из запроса
        album_form = AlbumForm(request.POST)
        # получение полей для настройки
        settings_form = NewAlbumForm(request.POST)

        # инициируем валидацию и очистку данных
        # без этого нельзя вытащить обработанные данные из .cleaned_data["имя_параметра"]
        settings_form.full_clean()

        # проверяем что форма верна
        if album_form.is_valid():
            # вытаскиваем поле "filename"(имя файла на сервере) из формы настроек
            filename = settings_form.cleaned_data["filename"]
            # вытаскиваем поле "to_db"(сохранить в базу данных) из формы настроек
            # оно будет сразу нужного типа bool вместо строки
            to_db = settings_form.cleaned_data["to_db"]

            # обработка ошибок что могут возникнуть при записи
            try:
                # если в форме отмечено что нужно сохранить в базу данных
                if to_db:
                    # сохраняем новую запись в базу данных
                    album_form.save()
                else:
                    # записываем json на диск
                    write_json(filename, album_form.cleaned_data)

                # отправляем сообщение что файл импортирован
                messages.success(request, "Создание завершен успешно")
            except Exception as e:
                # ловим ошибки при записе
                messages.error(request, f"ошибка при создании альбома {e}")

        else:
            # форма не верна, отправляем сообщение об ошибке
            messages.error(request, "Некоректные даннве из формы")
            messages.error(request, f"{album_form.errors.as_ul()}")
    else:
        # запрос был не "POST" отправляем сообщение с ошибкой
        messages.warning(request, "Неверный формат запроса")

    # создаем ответ с редиректом на главную страницу
    response = HttpResponseRedirect(  # создаем редирект
        reverse(
            # имя редиреакта из "urls.py"
            "index"
        )
    )
    # устанавливаем в куки что это первая вкладка
    response.set_cookie(COOKIE_ACTIVE_TAB, 1)
    return response


# вьюшка для импорта файла
# она не отображает свою страницу а перенаправляет на главную
def import_file(request):
    # проверяем что медод запроса "POST"
    if request.method == "POST":
        # получаем данные формы из запроса
        import_settings_form = ImportFileForm(
            data=request.POST,  # данные из формы
            files=request.FILES,  # файлы из формы
        )

        # проверяем что форма верна
        if import_settings_form.is_valid():
            # вытаскиваем данные файла из формы
            file = import_settings_form.cleaned_data["file"]
            # вытаскиваем поле "filename" из формы
            filename = import_settings_form.cleaned_data["filename"]
            # вытаскиваем поле "to_db"(сохранить в базу данных) из формы настроек
            # оно будет сразу нужного типа bool вместо строки
            to_db = import_settings_form.cleaned_data["to_db"]

            # обработка ошибок что могут возникнуть при работе с файлами
            try:
                # загружаем файл как json данные (на самомо деле в python то просто словарь ключ-значение)
                json_data = json.load(file)

                # проверяем что это json список а не объект
                if not isinstance(json_data, list):
                    messages.error(request, "JSON не содержит массив Альбомов")
                else:
                    if to_db:
                        import_file_to_db(request, json_data)
                    else:
                        import_file_to_server(request, json_data, filename, file)

            except Exception as e:
                # выводим сообщение об ошибке
                messages.error(request, f"{e}")

        else:
            # форма не верна, отправляем сообщение об ошибке
            messages.error(
                request,
                f"Некоректные даннве из формы\n{import_settings_form.errors.as_text()}",
            )
    else:
        # запрос был не "POST" отправляем сообщение с ошибкой
        messages.error(request, "Неверный формат запроса")

    # создаем ответ с редиректом на главную страницу
    response = HttpResponseRedirect(  # создаем редирект
        reverse(
            # имя редиреакта из "urls.py"
            "index"
        )
    )
    # устанавливаем в куки что это вторая вкладка
    response.set_cookie(COOKIE_ACTIVE_TAB, 2)
    return response


# импорт из json в базу данных
def import_file_to_db(request, json_data):
    # перебираем все элементы json массива
    for json_item in json_data:
        # конвертируем json данные в форму данных альбома
        albom = AlbumForm(
            data=json_item,  # данные из словаря json
        )
        # проверяем данные на валидность
        if albom.is_valid():
            # сохраняем
            albom.save()
            # отправляем сообщение что файл импортирован
            messages.success(request, "Импорт завершен успешно")
        else:
            # выводим сообщение об ошибке
            messages.error(request, f"{albom.errors.as_ul()}")
            messages.error(
                request,
                f"{json.dumps(json_item, indent = 4, ensure_ascii=False)}",
            )


# импорт из json на файл сервера
def import_file_to_server(request, json_data, filename, file):
    # если поле "filename" не задано
    if not filename:
        # имя фала остаеться изначальным
        filename = file.name

    # переменная для валидации файла
    file_is_valid = True

    # перебираем все элементы json массива
    for json_item in json_data:
        # конвертируем json данные в форму данных альбома
        albom = AlbumForm(
            data=json_item,  # данные из словаря json
        )

        # проверяем данные на валидность
        if not albom.is_valid():
            # ставим флаг что данныве невалидны
            file_is_valid = False
            # выводим сообщение
            messages.error(request, f"{albom.errors.as_ul()}")
            messages.error(
                request,
                f"{json.dumps(json_item, indent = 4, ensure_ascii=False)}",
            )

    # если файл прошел валидацию
    if file_is_valid:
        # записываем файл на диск
        write_file(filename, file)
        # отправляем сообщение что файл импортирован
        messages.success(request, "Импорт завершен успешно")
    else:
        # если файл непрошел валидацию
        # запрос был не "POST" отправляем сообщение с ошибкой
        messages.error(request, "Импорт неудался")


# вьбшка для скачивания файла
# нет своей страницы, просто качает файл
def download_file(request, filename):
    # создаем ответ с данными файла
    response = FileResponse(read_file(filename))
    # устанавливаем тип ответа "octet-stream" чтобы браузер качал файл а не открыл как страницу
    response["Content-Type"] = "application/octet-stream"
    # устанавливаем имя файла
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# вьбшка для удаления файла
# нет свое страницы, просто редирект на главную
def delete(request, filename):
    # удалям файл
    delete_file(filename)
    # создаем редирект
    response = HttpResponseRedirect(  # создаем редирект
        reverse(
            # имя редиреакта из "urls.py"
            "index"
        )
    )
    # устанавливаем в куки что это третья вкладка
    response.set_cookie(COOKIE_ACTIVE_TAB, 3)
    return response


# экспорт из базы данных в json
def export_file_from_db(request):
    # получаю все записи из базы данных
    all_albums = Album.objects.all()
    json_data = json_str(  # метод обвертка
        list(all_albums.values()),  # данные для сериализации в JSON
    )

    # создаем ответ с данными файла
    response = FileResponse(json_data)

    # устанавливаем тип ответа "octet-stream" чтобы браузер качал файл а не открыл как страницу
    response["Content-Type"] = "application/octet-stream"
    # устанавливаем имя файла
    response["Content-Disposition"] = (
        # передаем имя файла в браузер
        f'attachment; filename="albums-{datetime.now().isoformat()}.json"'
    )

    # устанавливаем в куки что это третья вкладка
    response.set_cookie(COOKIE_ACTIVE_TAB, 3)
    return response


# метод редактирования или удаления экземпляра записи базы данных
def action(request):
    # проверяем что медод запроса "POST"
    if request.method == "POST":
        # получаем данные формы из запроса
        action_form = ActionForm(
            data=request.POST,  # данные из формы
        )

        # валидируем данные из формы
        if action_form.is_valid():
            # получаем id альбома
            id = action_form.cleaned_data["id"]
            # получаем тип действия
            action = action_form.cleaned_data["action"]

            # получаем из базы данных запись с нужным id
            album = Album.objects.get(id=id)
            # связываем данные формы с записью из формы
            # чтобы можно было обновлять значения
            album_form = AlbumForm(
                data=request.POST,  # данные из формы
                instance=album,  # экземпляр днных из быза данных
            )

            # проверяем что форма верна
            if album_form.is_valid():
                # проверем тип операции
                if action == "delete":
                    # если удаление
                    # удаляем экземпляр данных из базы данных
                    album.delete()
                    # выводим сообщение об успехе
                    messages.info(request, f'Альбом #{id} "{album.title}" удален')
                elif action == "update":
                    # если сохранение
                    # сохраняем / обновляем экземпляр данных в базе данных
                    album.save()
                    # выводим сообщение об успехе
                    messages.info(request, f'Альбом #{id} "{album.title}" изменен')
                else:
                    # если действие неизвесно
                    # выводим сообщение об обшибке
                    messages.error(request, f'Неизвесный тип операции "{action}"')
            else:
                # выводим сообщение об обшибке если данный альбома невалидны
                messages.error(request, f"{album_form.errors.as_text()}")
        else:
            # выводим сообщение об обшибке если из формы не пришли нужные поля
            messages.error(request, f"{action_form.errors.as_text()}")

    # создаем редирект
    response = HttpResponseRedirect(  # создаем редирект
        reverse(
            # имя редиреакта из "urls.py"
            "index"
        )
    )
    # устанавливаем в куки что это третья вкладка
    response.set_cookie(COOKIE_ACTIVE_TAB, 0)
    return response


# вывод из базы данных в json ответ
def json_albums(request):
    if request.method == "POST":
        try:
            # вытаскиваем тело запроса и преобразуем его в json
            data = json.loads(request.body)
            # достаем флаг fromDb(из БД) из json
            from_db = data["fromDb"]
            # если получаем данные из БД
            if from_db:
                # достааем все данные альбомов из БД
                all_albums = Album.objects.all()
                json_data = json_str(  # метод обвертка
                    list(all_albums.values()),  # данные для сериализации в JSON
                )
                # возвращаем ответ
                return HttpResponse(
                    json_data, # даннве ответа
                    content_type="application/json", # формат ответа (бля того чтобы браузер знал что это)
                )
            else:
                # если получаем данные из файла

                # достаем имя файла
                filename = data["filename"]

                # если строка имени не пустое 
                if not str.isspace(filename):
                    # читаем json файл
                    json_data = json_str(read_json(filename))
                    # возвращаем ответ
                    return HttpResponse(
                        json_data, # даннве ответа
                        content_type="application/json", # формат ответа (бля того чтобы браузер знал что это)
                    )
                else:
                    # если имя файлы нету
                    # создаем объект словарь с ошибкой
                    error = {
                        "messaage": "имя файла не предоставлено"
                    }
                    # возвращаем ответ с ошибкой
                    return HttpResponse(
                        json_str(error), # даннве ответа
                        content_type="application/json", # формат ответа (бля того чтобы браузер знал что это)
                        status=404, # код ответа (404-ненайдено)
                    )
        except Exception as e:
            # ловим хоть одну ошибку
            # создаем объект словарь с ошибкой
            error = {
                "messaage": f"{e}"
            }
            # возвращаем ответ с ошибкой
            return HttpResponse(
                json_str(error), # даннве ответа
                content_type="application/json", # формат ответа (бля того чтобы браузер знал что это)
                status=500, # код ответа (500-внутренняя ошибка сервера)
            )
    

    # достааем все данные альбомов из БД
    all_albums = Album.objects.all()
    json_data = json_str(  # метод обвертка
        list(all_albums.values()),  # данные для сериализации в JSON
    )
    # возвращаем ответ
    return HttpResponse(
        json_data, # даннве ответа
        content_type="application/json", # формат ответа (бля того чтобы браузер знал что это)
    )
