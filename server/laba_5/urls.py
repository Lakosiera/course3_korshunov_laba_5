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
        view=views.create,  # вьюшка из файла 'views.py'
        name="create", 
    ),
    path(
        route="upload",  # путь
        view=views.import_file,  # вьюшка из файла 'views.py'
        name="upload", 
    ),
    path(
        route="export",  # путь  (т.е. /export")
        view=views.export,  # вьюшка из файла 'views.py'
        name="export", 
    ),
]
