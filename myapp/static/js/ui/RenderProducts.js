export function renderProducts(data) {
  const auctions = document.getElementById("auctions");
  auctions.innerHTML = "";
  console.log(data.Error);

  if (data.Error) {
    console.log("odf");
    auctions.innerHTML = `<p>${data.Error}</p>`;
  }

  const route = window.location.pathname;
  if (!route.includes("my")) {
    data.products.forEach((product) => {
      auctions.innerHTML += `
      <div>
        <h3>${product.product_name}</h3>
        <p>${product.description || "Sem descrição"}</p>
        <p>Min Bid: ${product.min_bid ?? "N/A"}</p>
        <p>Category: ${product.category || "Sem categoria"}</p>
        <button class="join-auction" data-room-token="${product.room}">
          Join Auction
        </button>
      </div>`;
    });
  } else {
    data.products.forEach((product) => {
      auctions.innerHTML += `
      <div>
        <h3>${product.product_name}</h3>
        <p>${product.description || "Sem descrição"}</p>
        <p>Date: ${product.start_datetime ?? "N/A"}</p>
      </div>`;
    });
  }

  document.querySelectorAll(".join-auction").forEach((btn) => {
    btn.addEventListener("click", (e) => joinRoom(e));
  });
}
