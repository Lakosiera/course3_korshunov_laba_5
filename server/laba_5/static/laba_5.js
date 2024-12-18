window.addEventListener('load', () => {
    onInit()
})


function onInit() {
    const showFromDb = document.getElementById("showFromDb")
    const addToDb = document.getElementById("addToDb")
    const importToDb = document.getElementById("importToDb")

    initSearch()

    showFromDb.onchange = (event) => {
        // console.log(event.currentTarget.checked)
        getJson("/albums")
            .then((data) => data.json())
            .then((data) => {
                console.log(data)
            })
            .catch(console.log)
    };
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


async function getJson(url) {
    return await fetch(url, {
        method: "POST",
        headers: {
            // DOCS: https://docs.djangoproject.com/en/5.1/howto/csrf/#using-csrf-protection-with-ajax
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-type": "application/json",
        },
        body: JSON.stringify({ username: "test" }),
    })
}

function getCookie(key) {
    return document.cookie
        .split(";")
        .map((item) => item.trim())
        .find((item) => item.startsWith(`${key}=`))
        ?.split("=")[1]
}

function setCookie(key, value) {
    document.cookie = `${key}=${value}`
}