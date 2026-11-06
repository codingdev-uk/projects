const slider = document.querySelector(".slider-container input");
const imageWrapper = document.querySelector(".image-wrapper");

slider.addEventListener("input", (e) => {imageWrapper.style.width = e.target.value + "%"; console.log(e.target.value);});
