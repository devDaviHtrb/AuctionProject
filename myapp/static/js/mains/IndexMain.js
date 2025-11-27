import { nextSlide } from "../interactivity/NextSlide.js";
import { prevSlide } from "../interactivity/PrevSlide.js";

let index = 0;
const slides = Array.from(document.querySelectorAll(".slide"));
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");

if (prevButton && nextButton) {
  prevButton.addEventListener("click", () => {
    index = prevSlide(index, slides);
  });

  nextButton.addEventListener("click", () => {
    index = nextSlide(index, slides);
  });
}

document.querySelectorAll(".slide").forEach(slide => {
  slide.addEventListener("click", () => {
    const filter = slide.dataset.filter;
    sessionStorage.setItem("filterCarrousel", filter);
    window.location.href = "/auctions";
  });
});

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const days = Math.floor(totalSeconds / (3600 * 24));
  const hours = Math.floor((totalSeconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const parts = [];
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  parts.push(`${seconds}s`);

  return parts.join(" ");
}

function setupTimer(element, relatedButton) {
  const startTime = new Date(element.dataset.start).getTime();
  const durationMinutes = parseFloat(element.dataset.duration);
  const durationMs = durationMinutes * 60 * 1000;

  let endTime = startTime + durationMs;
  if (element.dataset.dynamicEndTime) {
    endTime = parseInt(element.dataset.dynamicEndTime);
  }

  const timerText = element.querySelector('.timer-text') || element;

  function updateTimer() {
    const now = Date.now();

    if (element.dataset.dynamicEndTime) {
      endTime = parseInt(element.dataset.dynamicEndTime);
    }

    if (now < startTime) {
      timerText.textContent = `Começa em ${formatTime(startTime - now)}`;
      timerText.style.color = "#007bff";
      relatedButton.disabled = true;
      relatedButton.textContent = "AGUARDANDO";

    } else if (now >= startTime && now <= endTime) {
      timerText.textContent = `Tempo restante: ${formatTime(endTime - now)}`;
      timerText.style.color = "#28a745";
      relatedButton.disabled = false;
      relatedButton.textContent = "DAR LANCE";

    } else {
      timerText.textContent = "ENCERRADO";
      timerText.style.color = "#dc3545";
      relatedButton.disabled = true;
      relatedButton.textContent = "ENCERRADO";
      clearInterval(interval);
    }
  }

  updateTimer();
  const interval = setInterval(updateTimer, 1000);
}



document.addEventListener("DOMContentLoaded", () => {
  const recommendedTimers = document.querySelectorAll('.recommended-timer');

  recommendedTimers.forEach(timer => {
    const button = timer.closest('.product-card').querySelector('.btn-bid');
    if (button) setupTimer(timer, button);
  });
});
