// обработчик события завершения загрузки старницы 
window.addEventListener('load', () => {
    // выполняем инициацию
    onInit()
})

// константы
// источник данных из БД или файла
const COOKIE_DB_KEY = "laba_5_from_db"
// имя файла на севрер
const COOKIE_FILENAME_KEY = "laba_5_filename"
//  активаная вкладка
const COOKIE_ACTIVE_TAB = "laba_5_tab"

// инициация всего
function onInit() {
    // получаем флаг из куки для определения источника данных
    let fromDb = getCookie(COOKIE_DB_KEY, true) == 'true'
    // получаем имя файла на сервере
    let filename = getCookie(COOKIE_FILENAME_KEY, "albums.json")
    // переменная для строки поиска
    let search = null

    // получаем инпут поиска
    const searchInput = document.getElementById("searchInput")
    // получаем инпут имени файла на сервере
    const filenameInput = document.getElementById("filenameInput")
    // ошибки
    const errorMsg = document.getElementById("errorMsg")

    // в зависимости от источника данных отключаем поиск
    searchDisable(searchInput, fromDb)
    // в зависимости от источника данных отключаем имя файла
    searchDisable(filenameInput, !fromDb)
    // инциируем шаблон для таблицы
    const tmpl = initTemplate("tmplDataTableRow", "dataTableContainer")
    // обновляем данные в таблице
    updateDataView(tmpl, errorMsg, fromDb, filename)

    // инициирцем флаги источника данных
    // получаем чекбокс
    const showFromDb = document.getElementById("showFromDb")
    // все чекбоксы
    const checkBoxes = [
        showFromDb,
        document.getElementById("addToDb"),
        document.getElementById("importToDb")
    ]
    // переберираем чекбоксы
    checkBoxes.forEach((cb) => {
        // выстанавливаем значение из куки
        cb.checked = fromDb
        // подписываем на эвент изменения
        cb.onchange = (event) => {
            // меняем переменную флага источника данных
            fromDb = event.currentTarget.checked
            // сохраняем куки
            setCookie(COOKIE_DB_KEY, fromDb)

            // в зависимости от источника данных отключаем поиск
            searchDisable(searchInput, fromDb)
            // в зависимости от источника данных отключаем имя файла
            searchDisable(filenameInput, !fromDb)
            // обновляем данные в таблице
            updateDataView(tmpl, errorMsg, fromDb, filename, search)

            // для кадого чекбокса меняем значение
            checkBoxes.forEach((cb) => {
                cb.checked = fromDb
            })
        }
    })


    // записываем имя файла что сохранено в куки
    filenameInput.value = filename
    // вешаем обработчик событий на изменение значения
    filenameInput.addEventListener("input", (event) => {
        // получаем имя файла на сервере
        filename = event.target.value
        // сохраняем в куки
        setCookie(COOKIE_FILENAME_KEY, filename)
        // обновляем данные в таблице
        updateDataView(tmpl, errorMsg, fromDb, filename, search)
    })

    // инициирцем поиск
    // вешаем обработчик событий на изменение значения
    searchInput.addEventListener("input", (event) => {
        // получаем строку для поиска из эвента
        search = event.target.value
        // обновляем поля таблицы
        updateDataView(tmpl, errorMsg, fromDb, filename, search)
    })
}

// отклюяаем инпут в заисимости от флага
function searchDisable(input, flag) {
    if (flag) {
        input.removeAttribute("disabled")
    } else {
        input.setAttribute("disabled", "")
    }
}

// обновляем данные в таблице
function updateDataView(tmpl, errorMsg, fromDb, filename, search = null) {
    // получаем данные
    getJson(
        // url запроса
        "/albums",
        // тело запроса
        {
            fromDb, filename, search
        },
    )
        // преобразуем данные d json
        .then((data) => data.json())
        // обновляем шаблом полученными данными
        .then((data) => tmpl(data))
        .catch((err) => {
            // обрабатываем ошибки
            errorMsg.appendChild(alertMsg(err))
        })
}

// создаем нод с тектсом ошибки
function alertMsg(err) {
    const htmlStr=`
    <div class="mt-3 alert alert-dismissible fade show alert-danger">
        <div class="text-start">
        ${err}
        </div>
        <button type="button" data-bs-dismiss="alert" aria-label="Close" class="btn-close"></button>
    </div>
    `
    //  парсер
    const parser = new DOMParser();
    // парсим секст как html
    const alert = parser.parseFromString(htmlStr, "text/html");
    // так как это html то нужный нод надо вытащить из body
    return alert.body.childNodes[0]
}


// инициируем шаблон
function initTemplate(id, rootId) {
    // вытаскиваем нод который будет использоваться в качестве шаблона
    const tmpl = document.getElementById(id)
    // получаем нод куда будем запихивать данные
    const root = document.getElementById(rootId)
    // возврашщаем функцию с помощию которой будем заполнять нод контейнер шаблонами с данными
    return (data) => {
        // очищаем все ноды что уже были 
        root.innerHTML = ""
        // перебирвем данные в массиве
        data.forEach((row) => {
            // добавляем новый экземпляр шаблона с данными
            root.appendChild(albumTemplate(tmpl, row))
        });
    }
}

// заполнение шаблона данными
function albumTemplate(tmpl, data) {
    // клонируем нод шаблона (иначе будет просто переписывать один и тот же нод)
    const clone = tmpl.content.cloneNode(true)

    // получаем инпуты из шаблона
    const tmplTitle = clone.getElementById("tmplTitle")
    const tmplArtist = clone.getElementById("tmplArtist")
    const tmplRelesasedAt = clone.getElementById("tmplRelesasedAt")
    const tmplTracks = clone.getElementById("tmplTracks")
    const tmplGenre = clone.getElementById("tmplGenre")
    const tmplType = clone.getElementById("tmplType")

    // получаем кнопку редактирования из шаблона
    const tmplEdit = clone.getElementById("tmplEdit")
    // получаем модальное окно из шаблона
    const tmplModal = clone.getElementById("tmplModal")

    // получаем инпуты из имодального окна
    const modalLabel = clone.getElementById("modalLabel")
    const modalId = clone.getElementById("modalId")
    const modalTitle = clone.getElementById("modalTitle")
    const modalArtist = clone.getElementById("modalArtist")
    const modalRelesasedAt = clone.getElementById("modalRelesasedAt")
    const modalTracks = clone.getElementById("modalTracks")
    const modalGenre = clone.getElementById("modalGenre")
    const modalType = clone.getElementById("modalType")

    // если в данных нет поля id
    if (!data.id) {
        // прячем кнопку редактировать запись
        tmplEdit.classList.add("invisible")
    }

    // id для модального окна
    const id = data.id || getRandomInt(1000000)

    // связываем модальное окно с кнопкой через уникальный id
    tmplEdit.setAttribute('data-bs-target', `#tmplModal-${id}`)
    tmplModal.setAttribute('id', `tmplModal-${id}`)

    // запоняем данные в таблице
    tmplTitle.textContent = data.title
    tmplArtist.textContent = data.artist
    tmplRelesasedAt.textContent = data.relesased_at
    tmplTracks.textContent = data.tracks
    tmplGenre.textContent = data.genre
    tmplType.textContent = data.type
    tmplTracks.textContent = data.tracks

    // заполняем данные в модальном окне
    modalLabel.textContent += data.id
    modalId.value = data.id
    modalTitle.value = data.title
    modalArtist.value = data.artist
    modalRelesasedAt.value = data.relesased_at
    modalTracks.value = data.tracks
    modalGenre.value = data.genre
    modalType.value = data.type
    modalTracks.value = data.tracks

    // возвращаем клон шаблона заполненного данными
    return clone
}

// POST запрос в Django
function getJson(url, body) {
    return fetch(url, {
        method: "POST", // метод запроса
        headers: { // хэдеры запроса
            // DOCS: https://docs.djangoproject.com/en/5.1/howto/csrf/#using-csrf-protection-with-ajax
            // так как Django использует сессии для идентификации передаем значение сесии из куки
            "X-CSRFToken": getCookie("csrftoken"), 
            // тип отправляемых данных
            "Content-type": "application/json",
        },
        // тело запроса json конвертированный в текстовый формат
        body: JSON.stringify(body),
    })
}

// получение куки
function getCookie(key, defValue = null) {
    return document.cookie
        .split(";") // делим строку на масив (; - в качестве разделителя)
        .map((item) => item.trim()) // убераем пробелы в элементах массива (отступы в начали или конце)
        .find((item) => item.startsWith(`${key}=`)) // ищем элемент который начинаеться на "ключ="
        ?.split("=")[1] || defValue // если нашли вернум все что было после "=" иначе значчение "defValue"
}

// сохраняем куки
function setCookie(key, value) {
    document.cookie = `${key}=${value}`
}

// рандомное целое число от 0 до max
function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

// сохраняем номер вкладки в куки
function setTab(index) {
    setCookie(COOKIE_ACTIVE_TAB, index)
}