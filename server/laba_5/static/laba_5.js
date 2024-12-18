window.addEventListener('load', () => {
    onInit()
})


function onInit() {
    const showFromDb = document.getElementById("showFromDb")
    const addToDb = document.getElementById("addToDb")
    const importToDb = document.getElementById("importToDb")

    showFromDb.onchange = (event) => {
        console.log(event.currentTarget.checked)
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