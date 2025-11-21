import { nextSlide } from "../interactivity/NextSlide.js";
import { prevSlide } from "../interactivity/PrevSlide.js";

let index = 0;
const slides = Array.from(document.querySelectorAll(".slide"));
console.log("foi")
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");

prevButton.addEventListener("click", () => {
  index = prevSlide(index, slides);
});

nextButton.addEventListener("click", () => {
  index = nextSlide(index, slides);
});

document.querySelectorAll(".slide").forEach((slide) => {
  slide.addEventListener("click", () => {
    const filter = slide.dataset.filter;
    sessionStorage.setItem("filterCarrousel", filter);
    window.location.href = "/auctions";
  });
});


