import { showSlide } from "./ShowSlide.js";

export function prevSlide(index, slides) {
  index = (index - 1 + slides.length) % slides.length; // 👈 evita valor negativo
  showSlide(index, slides);
  return index; // 👈 devolve o novo índice
}
