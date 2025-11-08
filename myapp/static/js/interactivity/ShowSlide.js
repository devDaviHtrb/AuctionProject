export function showSlide(i, slides) {
  slides.forEach((slide, n) => {
    slide.classList.toggle("active", n === i);
  });

  const slidesContainer = document.querySelector(".slides");
  slidesContainer.style.transform = `translateX(-${i * 100}%)`;
}
