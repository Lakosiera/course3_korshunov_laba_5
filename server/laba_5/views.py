from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.contrib import messages
import json
from .forms import MusicAlbumForm, ImportFileForm

# имя куки для хранения номера вкладки
COOKIE_ACTIVE_TAB = "laba_5_tab"


# пример простейшей вьющки
def hello_world(request):
    # простейший вывод html страницы
    return HttpResponse("Hello, world!")


# вьбшка главной страници
def index(request):
    # получаем из куки на какой вкладке мы были
    tab_index = request.COOKIES.get(COOKIE_ACTIVE_TAB, "0")
    # передаем данные контекста
    context = {
        # параметр заголовока
        "name": "Laba 5 - Музыкальные альбомы",
        # интекс вкладки
        "tab_index": tab_index,
    }
    # ренедр вьюшки в html страницу
    return render(request, "index.html", context)


# вьюшка для создания альбома
# она не отображает свою страницу а перенаправляет на главную
def create(request):
    # проверяем что медод запроса "POST"
    if request.method == "POST":
        # получаем данные формы из запроса
        form = MusicAlbumForm(request.POST)

        # проверяем что форма верна
        if form.is_valid():
            # обработка ошибок что могут возникнуть при записи
            try:
                # записываем json на диск
                # TODO write_json
                # write_json(filename, form.cleaned_data)

                # отправляем сообщение что файл импортирован
                messages.success(request, "Создание завершен успешно")
            except Exception as e:
                # ловим ошибки при записе
                messages.error(request, f"ошибка при создании альбома{e}")

        else:
            # форма не верна, отправляем сообщение об ошибке
            messages.error(request, "Некоректные даннве из формы")
            messages.error(request, f"{form.errors.as_ul()}")
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
    response.set_cookie(COOKIE_ACTIVE_TAB, 0)
    return response


# вьюшка для импорта файла
# она не отображает свою страницу а перенаправляет на главную
def import_file(request):
    # проверяем что медод запроса "POST"
    if request.method == "POST":
        # получаем данные формы из запроса
        form = ImportFileForm(
            data=request.POST, # данные из формы
            files=request.FILES, # файлы из формы
        )

        # проверяем что форма верна
        if form.is_valid():
            # вытаскиваем данные файла из формы
            file = form.cleaned_data["file"]

            # обработка ошибок что могут возникнуть при работе с файлами
            try:
                # переменная для валидации файла
                file_is_valid = True
                # загружаем файл как json данные (на самомо деле в python то просто словарь ключ-значение)
                json_data = json.load(file)

                if not isinstance(json_data, list):
                    file_is_valid = False
                    messages.error(request, "JSON не содержит массив Альбомов")

                # перебираем все элементы json массива
                for json_item in json_data:
                    # конвертируем json данные ворму данных альбома
                    albom = MusicAlbumForm(
                        data=json_item # данные из словаря json
                    )
                    # проверяем данные на валидность
                    if not albom.is_valid():
                        # ставим флаг что данныве невалидны
                        file_is_valid = False
                        # выводим сообщение
                        messages.error(request, f"{albom.errors.as_ul()}")
                        messages.error(request, f"{json.dumps(json_item, indent = 4, ensure_ascii=False)}")
                        
                # если файл прошел валидацию
                if file_is_valid:
                    # записываем файл на диск
                    # TODO 
                    # write_file(filename, file)

                    # отправляем сообщение что файл импортирован
                    messages.success(request, "Импорт завершен успешно")
                else:
                    # если файл непрошел валидацию
                    # запрос был не "POST" отправляем сообщение с ошибкой
                    messages.error(request, "Импорт неудался")
            except Exception as e:
                # выводим сообщение об ошибке
                messages.error(request, f"{e}")

        else:
            # форма не верна, отправляем сообщение об ошибке
            messages.error(request, f"Некоректные даннве из формы\n{form.errors.as_text()}")
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
    response.set_cookie(COOKIE_ACTIVE_TAB, 1)
    return response


# вьюшка для скачивания файла
# нет своей страницы, просто качает файл
def export(request):
    # TODO 
    # создаем ответ с данными файла
    response = Http404() # FileResponse(read_file(filename))
    # # устанавливаем тип ответа "octet-stream" чтобы браузер качал файл а не открыл как страницу
    # response["Content-Type"] = "application/octet-stream"
    # # устанавливаем имя файла
    # response["Content-Disposition"] = f'attachment; filename="{"filename"}"'
    return response
