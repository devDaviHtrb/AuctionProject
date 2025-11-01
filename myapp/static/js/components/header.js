const suggestions = [
    "Rolex Submariner",
    "iPhone 15 Pro Max",
    "PlayStation 5",
    "MacBook Pro M3",
    "Ferrari F8 Tributo",
    "Câmera Canon EOS R6",
    "Smart TV Samsung 65''",
    "Patek Philippe Nautilus",
    "Lamborghini Huracán",
    "Gucci Handbag",
    "Yamaha R1",
    "Tesla Model S",
    "AirPods Pro 2",
    "Apple Watch Ultra",
    "Bicicleta Specialized Tarmac"
];

const searchInput = document.getElementById("searchInput");
const listContainer = document.getElementById("autocompleteList");

let currentFocus = -1;

searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();
    listContainer.innerHTML = "";

    if (!query) return;

    const filtered = suggestions.filter(item =>
        item.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
        listContainer.innerHTML = "<div class='autocomplete-item'>Sem resultados</div>";
        return;
    }

    filtered.forEach((item) => {
        const div = document.createElement("div");
        div.classList.add("autocomplete-item");
        div.textContent = item;
        div.addEventListener("click", function () {
            searchInput.value = item;
            listContainer.innerHTML = "";
        });
        listContainer.appendChild(div);
    });
});

searchInput.addEventListener("keydown", function (e) {
    let items = listContainer.getElementsByClassName("autocomplete-item");
    if (e.key === "ArrowDown") {
        currentFocus++;
        addActive(items);
    } else if (e.key === "ArrowUp") {
        currentFocus--;
        addActive(items);
    } else if (e.key === "Enter") {
        e.preventDefault();
        if (currentFocus > -1 && items[currentFocus]) {
            items[currentFocus].click();
        }
    }
});

function addActive(items) {
    if (!items) return;
    removeActive(items);
    if (currentFocus >= items.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = items.length - 1;
    items[currentFocus].classList.add("active");
}

function removeActive(items) {
    for (let item of items) item.classList.remove("active");
}

document.addEventListener("click", function (e) {
    if (!e.target.closest(".search-bar")) listContainer.innerHTML = "";
});
const userButton = document.getElementById("userButton");
const dropdownMenu = document.getElementById("dropdownMenu");

userButton.addEventListener("click", (e) => {
  e.stopPropagation(); // evita fechar ao clicar no botão
  dropdownMenu.classList.toggle("hidden");
});

// Fechar menu ao clicar fora
document.addEventListener("click", (e) => {
  if (!dropdownMenu.contains(e.target) && !userButton.contains(e.target)) {
    dropdownMenu.classList.add("hidden");
  }
});
