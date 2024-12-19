window.addEventListener('load', () => {
    onInit()
})

const COOKIE_DB_KEY = "laba_5_from_db"
const COOKIE_ACTIVE_TAB = "laba_5_tab"

function onInit() {
    const showFromDb = document.getElementById("showFromDb")

    initCheckboxes([
        showFromDb, 
        document.getElementById("addToDb"), 
        document.getElementById("importToDb")
    ])

    const tmpl = initTemplate("tmplDataTableRow", "dataTableContainer")
    const filename = "albums.json"

    const fromDb = getCookie(COOKIE_DB_KEY, true) == 'true'
    updateDataView(tmpl, fromDb, "albums.json")

    showFromDb.addEventListener("change", (event) => {
        updateDataView(tmpl, event.currentTarget.checked, filename)
    })
}

function initCheckboxes(checkBoxes) {
    let fromDb = getCookie(COOKIE_DB_KEY, true)

    checkBoxes.forEach((cb) => {
        cb.checked = fromDb == 'true'
        cb.onchange = (event) => {
            fromDb = event.currentTarget.checked
            setCookie(COOKIE_DB_KEY, fromDb)
            checkBoxes.forEach((cb) => {
                cb.checked = event.currentTarget.checked
            })
        }
    })
}

function updateDataView(tmpl, fromDb, filename) {
    getJson(
        "/albums",
        {
            fromDb, filename
        },
    )
        .then((data) => data.json())
        .then((data) => {
            tmpl(data)
            // console.log(data)
        })
        .catch(console.log)
}

function initSearch() {
    const searchTitle = document.getElementById("searchTitle")
    const searchArtist = document.getElementById("searchArtist")
    const searchTracks = document.getElementById("searchTracks")
    const searchGenre = document.getElementById("searchGenre")
    const searchType = document.getElementById("searchType")


    searchTitle.oninput = (event) => {
        // console.log(event.currentTarget.value)
    };
}

function initTemplate(id, rootId) {
    const tmpl = document.getElementById(id)
    const root = document.getElementById(rootId)
    return (data) => {
        root.innerHTML = ""
        data.forEach((row) => {
            root.appendChild(albumTemplate(tmpl, row))
        });
    }
}

function albumTemplate(tmpl, data) {
    const clone = tmpl.content.cloneNode(true)
    const tmplTitle = clone.getElementById("tmplTitle")
    const tmplArtist = clone.getElementById("tmplArtist")
    const tmplRelesasedAt = clone.getElementById("tmplRelesasedAt")
    const tmplTracks = clone.getElementById("tmplTracks")
    const tmplGenre = clone.getElementById("tmplGenre")
    const tmplType = clone.getElementById("tmplType")

    const tmplEdit = clone.getElementById("tmplEdit")
    const tmplModal = clone.getElementById("tmplModal")

    const modalLabel = clone.getElementById("modalLabel")
    const modalId = clone.getElementById("modalId")
    const modalTitle = clone.getElementById("modalTitle")
    const modalArtist = clone.getElementById("modalArtist")
    const modalRelesasedAt = clone.getElementById("modalRelesasedAt")
    const modalTracks = clone.getElementById("modalTracks")
    const modalGenre = clone.getElementById("modalGenre")
    const modalType = clone.getElementById("modalType")

    if (!data.id) {
        tmplEdit.classList.add("invisible")
    }

    const id = data.id || getRandomInt(1000000)

    tmplEdit.setAttribute('data-bs-target', `#tmplModal-${id}`)
    tmplModal.setAttribute('id', `tmplModal-${id}`)

    tmplTitle.textContent = data.title
    tmplArtist.textContent = data.artist
    tmplRelesasedAt.textContent = data.relesased_at
    tmplTracks.textContent = data.tracks
    tmplGenre.textContent = data.genre
    tmplType.textContent = data.type
    tmplTracks.textContent = data.tracks

    modalLabel.textContent += data.id
    modalId.value = data.id
    modalTitle.value = data.title
    modalArtist.value = data.artist
    modalRelesasedAt.value = data.relesased_at
    modalTracks.value = data.tracks
    modalGenre.value = data.genre
    modalType.value = data.type
    modalTracks.value = data.tracks

    return clone
}

async function getJson(url, body) {
    return await fetch(url, {
        method: "POST",
        headers: {
            // DOCS: https://docs.djangoproject.com/en/5.1/howto/csrf/#using-csrf-protection-with-ajax
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-type": "application/json",
        },
        body: JSON.stringify(body),
    })
}

function getCookie(key, defValue = null) {
    return document.cookie
        .split(";")
        .map((item) => item.trim())
        .find((item) => item.startsWith(`${key}=`))
        ?.split("=")[1] || defValue
}

function setCookie(key, value) {
    document.cookie = `${key}=${value}`
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function setTab(index) {
    setCookie(COOKIE_ACTIVE_TAB, index)
}