let currentIndex = 0;

const slides = document.querySelectorAll('.slide');
const previousButton = document.querySelector('.previous-button');
const nextButton = document.querySelector('.next-button');

function showSlide(index) {
  slides.forEach(img => img.style.display = 'none');
  slides[index].style.display = 'block';
}

previousButton.addEventListener('click', () => { currentIndex = (currentIndex - 1 + slides.length) % slides.length; 
showSlide(currentIndex); 
});

nextButton.addEventListener('click', () => {currentIndex = (currentIndex + 1) % slides.length;
showSlide(currentIndex);
});


