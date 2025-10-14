export function showSlide(i, slides) {
  slides.forEach((slide, n) => {
    slide.classList.toggle("active", n === i);
  });
  document.querySelector(".slides").style.transform = `translateX(-${
    i * 100
  }%)`;
}
