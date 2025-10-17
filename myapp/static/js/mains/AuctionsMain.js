import { loadProducts } from "../interactivity/Paginate.js";

let currentPage = 1;
let currentFilter = document.getElementById("categories");

document.addEventListener("DOMContentLoaded", async () => {
  const filterCarroussel = sessionStorage.getItem("filterCarrousel"); //
  console.log(filterCarroussel);
  if (filterCarroussel) {
    sessionStorage.removeItem("filterCarrousel");

    if (currentFilter) {
      const option = [...currentFilter.options].find(
        (opt) => opt.value === filterCarroussel
      );
      if (option) option.selected = true;
    }

    await loadProducts(1, filterCarroussel);
  } else {
    await loadProducts(currentPage);
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
