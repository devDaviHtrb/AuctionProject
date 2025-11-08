import { showSlide } from "./ShowSlide.js";

export function prevSlide(index, slides) {
  index = (index - 1 + slides.length) % slides.length; 
  showSlide(index, slides);
  return index; 
}
