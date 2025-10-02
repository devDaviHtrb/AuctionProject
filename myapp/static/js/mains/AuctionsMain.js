import { loadProducts } from "../interactivity/Paginate";

let currentPage = 1;
let currentFilter = document.getElementById("categories");

document
  .getElementById("prev-btn")
  .addEventListener(
    "click",
    async () =>
      (currentPage = await loadProducts(currentPage - 1, currentFilter.value))
  );
document
  .getElementById("next-btn")
  .addEventListener(
    "click",
    async () =>
      (currentPage = await loadProducts(currentPage + 1, currentFilter.value))
  );
currentFilter.addEventListener("change", (e) => {
  currentPage = 1;
  loadProducts(currentPage, e.target.value);
});

document.addEventListener("DOMContentLoaded", () => {
  loadProducts(currentPage, currentFilter.value);
});
