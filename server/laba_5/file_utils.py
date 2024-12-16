from os import listdir, path, remove
import json


# директория для хранения медиафайлов
STOTRAGE_FOLDER = "/storage"


# метод для записи json файла
def write_json(filename, data):
    jsonfile = f"{STOTRAGE_FOLDER}/{filename}.json"
    # если файл уже существует
    if path.isfile(jsonfile):
        # читаем json файл (+ - запись в файл включена)
        with open(jsonfile,'r+', encoding='utf8') as infile:
            # читам json из фала
            json_data = json.load(infile)
            # добавляем запись в массив
            json_data.append(data)
            # перемещаемся в начало файла (чтбы переписать содержимое)
            infile.seek(0)
            # перезаписываем файл
            json.dump(json_data, infile, indent = 4, ensure_ascii=False)
    else:
        # если файла не существует создаем файл
        with open(jsonfile, "w", encoding='utf8') as outfile:
            # создаем josn с пустым массивом
            json_data = json.loads("[]")
            # добавляем запись в массив
            json_data.append(data)
            # записываем json в файл (с ворматированием отступов 4 пробела)
            json.dump(json_data, outfile, indent = 4, ensure_ascii=False)


# метод для записи файла
def write_file(filename, file):
    # открыть файл для "w" - записи, "b" - как бинарный файл
    with open(f"{STOTRAGE_FOLDER}/{filename}", "wb+") as destination:
        # для каждого "кусочка" (chunk) данных
        for chunk in file.chunks():
            # записываем в 
            destination.write(chunk)


# метод для чтения файла
def read_file(filename):
    # открыть файл для "r" - чтения, "b" - как бинарный файл
    return open(f"{STOTRAGE_FOLDER}/{filename}", 'rb')


# метод для удаления файла
def delete_file(filename):
    file = f"{STOTRAGE_FOLDER}/{filename}"
    # если файл существует
    if path.exists(file):
        # удаляем
        remove(file)


# метод для чтения директории
def read_dir():
    # читаем содержимое директории
    dir_list = listdir(path.abspath(STOTRAGE_FOLDER))
    # подгатавливаем пустой список результата
    result = []
    # перебираем все имена файлов из директории
    for filename in dir_list:
        # добавляем в результат имя файла
        result.append(filename)
    # возврвщвем результат
    return result
    