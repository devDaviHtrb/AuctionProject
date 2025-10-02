import { joinRoom } from "../sockets/JoinRoom";
export function renderProducts(data) {
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
    btn.addEventListener("click", (e) => joinRoom(e));
  });
}
