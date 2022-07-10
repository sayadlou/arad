function relocate_home() {
    document.getElementById("myframe").src = "home.html";
}

function relocate_portfolio() {
    document.getElementById("myframe").src = "portfolio.html";
}

function relocate_skills() {
    document.getElementById("myframe").src = "skills.html";
}

function relocate_experiences() {
    document.getElementById("myframe").src = "experiences.html";
}

function relocate_education() {
    document.getElementById("myframe").src = "education.html";
}

function bg_dark() {
    document.querySelector(".sidebar").classList.toggle("sidebar_dark");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function mobileMenu() {
    const menu = document.getElementById("Menu");

    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }

}

function mobileMenuResize() {
    const menu = document.getElementById("Menu");
    if (window.matchMedia("(max-width: 992px)").matches) {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

window.onresize = mobileMenuResize;
