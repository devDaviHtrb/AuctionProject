import { nextSlide } from "../interactivity/NextSlide.js";
import { prevSlide } from "../interactivity/PrevSlide.js";

let index = 0;
const slides = Array.from(document.querySelectorAll(".slide"));

const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");

prevButton.addEventListener("click", () => {
  index = prevSlide(index, slides); // 👈 atualiza o index
});

nextButton.addEventListener("click", () => {
  index = nextSlide(index, slides); // 👈 idem
});
