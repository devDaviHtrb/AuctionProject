import { nextSlide } from "../interactivity/NextSlide.js";
import { prevSlide } from "../interactivity/PrevSlide.js";

let index = 0;
const slides = document.querySelectorAll(".slide");

const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");

prevButton.addEventListener("click", (e) => {
  console.log("kdsfjbsdf");
  prevSlide(index, slides);
});

nextButton.addEventListener("click", (e) => {
  nextSlide(index, slides);
});
