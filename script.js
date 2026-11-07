let currentIndex = 0;

const images = document.querySelectorAll('.image-slider img');
const previousButton = document.querySelector('.previous-button');
const nextButton = document.querySelector('.next-button');

function showImage(index) {
  images.forEach(img => img.style.display = 'none');
  images[index].style.display = 'block';
}

previousButton.addEventListener('click', () => { currentIndex = (currentIndex - 1 + images.length) % images.length; 
showImage(currentIndex); 
});

nextButton.addEventListener('click', () => {currentIndex = (currentIndex + 1) % images.length;
showImage(currentIndex);
});
