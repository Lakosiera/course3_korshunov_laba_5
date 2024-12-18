from django.urls import path

from . import views

# пути для модуля 'laba_5'
urlpatterns = [
    # корневой путь (т.е. "/" или "http://localhost:8004/")
    path(
        route="",  # путь
        view=views.index,  # вьюшка из файла 'views.py'
        name="index",  # условное имя пути
    ),
    path(
        route="create",  # путь
        view=views.add_album,  # вьюшка из файла 'views.py'
        name="create", 
    ),
    path(
        route="upload",  # путь
        view=views.import_file,  # вьюшка из файла 'views.py'
        name="upload", 
    ),
    path(
        route="download/<str:filename>",  # путь  (т.е. /download/1734359984-ДАННЫЕ_ДЛЯ_ИМПОРТА.json")
        view=views.download_file,  # вьюшка из файла 'views.py'
        name="download", 
    ),
    path(
        route="delete/<str:filename>",  # путь  (т.е. /delete/1734359984-ДАННЫЕ_ДЛЯ_ИМПОРТА.json")
        view=views.delete,  # вьюшка из файла 'views.py'
        name="delete", 
    ),
    path(
        route="export",  # путь  (т.е. /export")
        view=views.export_file_from_db,  # вьюшка из файла 'views.py'
        name="export", 
    ),
    path(
        route="action",  # путь  (т.е. /action")
        view=views.action,  # вьюшка из файла 'views.py'
        name="action", 
    ),
]
