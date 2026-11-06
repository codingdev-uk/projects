const slider = document.querySelector(".slider-container input");
const image = document.getElementById("image-2");

slider.addEventListener("input", (e) => {image.style.width = e.target.value + "%";});

