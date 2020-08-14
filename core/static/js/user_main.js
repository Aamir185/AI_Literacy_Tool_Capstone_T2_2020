document.getElementById("desc-block").onmouseover = function() {mouseOver()};
document.getElementById("desc-block").onmouseout = function() {mouseOut()};

function mouseOver(element) {
    element.classList.add("animate-change");
    element.classList.add("changed");
    element.classList.add("animated-fast");
}

function mouseOut(element) {
    element.classList.remove("animate-change");
    element.classList.remove("changed");
    element.classList.remove("animated-fast");
}