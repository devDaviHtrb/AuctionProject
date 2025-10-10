let index = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(i) {
  slides.forEach((slide, n) => {
    slide.classList.toggle('active', n === i);
  });
  document.querySelector('.slides').style.transform = `translateX(-${i * 100}%)`;
}

function nextSlide() {
  index = (index + 1) % slides.length;
  showSlide(index);
}

function prevSlide() {
  index = (index - 1 + slides.length) % slides.length;
  showSlide(index);
}
