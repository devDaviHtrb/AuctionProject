import { loadProducts } from "../interactivity/Paginate";

let currentPage = 1;
let currentFilter = document.getElementById("categories");

document.addEventListener("DOMContentLoaded", async () => {
  const filterCarrousel = sessionStorage.getItem("filterCarrousel");

  if (filtroCarrossel) {
    sessionStorage.removeItem("filterCarrousel");

    if (currentFilter) {
      const option = [...currentFilter.options].find(
        (opt) => opt.value === filterCarrousel
      );
      if (option) option.selected = true;
    }

    await loadProducts(1, filterCarrousel);
  } else {
    await loadProducts(currentPage, currentFilter.value);
  }
});

document.getElementById("prev-btn").addEventListener("click", async () => {
  currentPage = await loadProducts(currentPage - 1, currentFilter.value);
});

document.getElementById("next-btn").addEventListener("click", async () => {
  currentPage = await loadProducts(currentPage + 1, currentFilter.value);
});

currentFilter.addEventListener("change", (e) => {
  currentPage = 1;
  loadProducts(currentPage, e.target.value);
});
