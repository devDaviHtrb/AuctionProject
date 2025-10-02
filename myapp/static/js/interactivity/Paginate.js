let currentPage = 1;
let currentFilter = document.getElementById("categories");

async function loadProducts(page = 1, filter = "") {
  try {
    const response = await fetch(
      `/paginate?page=${page}&filter=${encodeURIComponent(filter)}`
    );
    const data = await response.json();

    let auctions = document.getElementById("auctions");
    auctions.innerHTML = "";

    data.products.forEach((product) => {
      auctions.innerHTML += `<div><h3>${product.product_name}</h3>
                       <p>${product.description}</p>
                       <p>Min Bid: ${product.min_bid}</p>
                       <p>Category: ${product.category}</p>
                        <button class="join-auction" data-room-token="${product.product_room}">
                        Join Auction
                         </button></div>`;
    });
    document.querySelectorAll(".join-auction").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const room = e.target.dataset.roomToken;
        socket.emit("join_room", room);
        window.location.href = `/auction/${room}`;
      });
    });

    if (currentPage == 1) {
      document.getElementById("prev-btn").disabled = true;
    } else {
      document.getElementById("prev-btn").disabled = false;
    }
    if (!data.has_next) {
      document.getElementById("next-btn").disabled = true;
    } else {
      document.getElementById("next-btn").disabled = false;
    }
    document.getElementById(
      "page-info"
    ).textContent = `Page ${data.current_page} of ${data.total_pages}`;

    currentPage = data.current_page;
  } catch (err) {
    console.error(err);
  }
}

document
  .getElementById("prev-btn")
  .addEventListener("click", () =>
    loadProducts(currentPage - 1, currentFilter.value)
  );
document
  .getElementById("next-btn")
  .addEventListener("click", () =>
    loadProducts(currentPage + 1, currentFilter.value)
  );
currentFilter.addEventListener("change", (e) => {
  currentPage = 1;
  loadProducts(currentPage, e.target.value);
});

document.addEventListener("DOMContentLoaded", () => {
  loadProducts(currentPage, currentFilter.value);
});
