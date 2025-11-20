const searchInput = document.getElementById("searchInput");
const listContainer = document.getElementById("autocompleteList");

let suggestions = [];  
let currentFocus = -1;

async function fetchSuggestions() {
    try {
        const response = await fetch('/get/searchs-info');
        if (!response.ok) throw new Error(`Erro: ${response.status} ${response.statusText}`);
        // [[name, link], ...]
        suggestions = await response.json();
        buildCategoriesList(suggestions);
    } catch (error) {
        console.error("Error :", error);
    }
}
function getType(str, p1, p2) {
    let start = -1;
    for (let i = 0; i < str.length; i++) {
        if (str[i] === p1) {
            start = i + 1;  
        } else if (str[i] === p2 && start !== -1) {
            return str.slice(start, i);
        }
    }

    return "";
}


fetchSuggestions();
function buildCategoriesList(list) {
    const ul = document.getElementById("categories-ul");
    ul.innerHTML = "";

    list.forEach(item => {
        console.log(getType(item[1], '?', '='))
        if(getType(item[1], '?', '=') === "category"){
            const li = document.createElement("li");
            const a  = document.createElement("a");
            
            a.textContent = item.name;
            a.href = item.link;
            a.innerHTML = item[0];
            li.appendChild(a);
            ul.appendChild(li);
        }
    });
}


searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();
    listContainer.innerHTML = "";
    currentFocus = -1;

    if (!query) return;

    const filtered = suggestions.filter(item =>
        item[0].toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
        listContainer.innerHTML = "<div class='autocomplete-item'>Sem resultados</div>";
        return;
    }

    filtered.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("autocomplete-item");
        div.textContent = item[0];

        div.addEventListener("click", function () {
            window.location.href = item[1];
        });

        listContainer.appendChild(div);
    });
});

searchInput.addEventListener("keydown", function (e) {
    let items = listContainer.getElementsByClassName("autocomplete-item");
    if (!items) return;

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
        } else {
            window.location.href = "/products?name=" + encodeURIComponent(searchInput.value);
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
    e.stopPropagation();
    dropdownMenu.classList.toggle("hidden");
});

document.addEventListener("click", (e) => {
    if (!dropdownMenu.contains(e.target) && !userButton.contains(e.target)) {
        dropdownMenu.classList.add("hidden");
    }
});
