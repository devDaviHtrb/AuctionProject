import { showSlide } from "./ShowSlide.js";

export function nextSlide(index, slides) {
  index = (index + 1) % slides.length;
  showSlide(index, slides);
}
