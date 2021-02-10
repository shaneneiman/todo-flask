function showForm () {
    let form = document.querySelector("#form")
    if (form.classList.contains("hidden")) {
        form.classList.remove("hidden")
    } else {
        form.classList.add("hidden")
    }
}

let button = document.querySelector("#button")
if (button) {
    button.addEventListener("click", showForm)
}