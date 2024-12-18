window.addEventListener('load', () => {
    onInit()
})


function onInit() {
    const showFromDb = document.getElementById("showFromDb")
    const addToDb = document.getElementById("addToDb")
    const importToDb = document.getElementById("importToDb")

    initSearch()

    showFromDb.onchange = (event) => {
        console.log(event.currentTarget.checked)
    };
}

function initSearch() {
    const searchTitle = document.getElementById("searchTitle")
    const searchArtist = document.getElementById("searchArtist")
    const searchTracks = document.getElementById("searchTracks")
    const searchGenre = document.getElementById("searchGenre")
    const searchType = document.getElementById("searchType")

    
    searchTitle.oninput  = (event) => {
        console.log(event.currentTarget.value)
    };
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