export function showSlide(i, slides) {
  // Ajusta classes de ativo/inativo
  slides.forEach((slide, n) => {
    slide.classList.toggle("active", n === i);
  });

  // Move o container .slides
  const slidesContainer = document.querySelector(".slides");
  slidesContainer.style.transform = `translateX(-${i * 100}%)`;
}
