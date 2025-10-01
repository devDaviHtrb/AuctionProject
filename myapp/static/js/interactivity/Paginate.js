
let currentPage = 1; 
let currentFilter = ''; 

async function loadProducts(page = 1, filter = '') {
  try {
    const response = await fetch(`/paginate?page=${page}&filter=${encodeURIComponent(filter)}`)
    const data = await response.json()

    let auctions = document.getElementById('auctions')
    auctions.innerHTML = '';

    data.products.forEach(product => {
      auctions.innerHTML += `<h3>${product.product_name}</h3>
                       <p>${product.description}</p>
                       <p>Min Bid: ${product.min_bid}</p>
                       <p>Category: ${product.category}</p>`
    });

    if (currentPage == 1){
        document.getElementById('prev-btn').disabled = true
    }else{
        document.getElementById('prev-btn').disabled = false
    }
    if (!data.has_next){
        document.getElementById('next-btn').disabled =true
    }else{
        document.getElementById('next-btn').disabled =false
    }
    document.getElementById('page-info').textContent = `Page ${data.current_page} of ${data.total_pages}`

    currentPage = data.current_page; 
  } catch (err) {
    console.error(err);
  }
}

document.getElementById('prev-btn').addEventListener('click', () => loadProducts(currentPage - 1, currentFilter))
document.getElementById('next-btn').addEventListener('click', () => loadProducts(currentPage + 1, currentFilter))


document.addEventListener("DOMContentLoaded", ()=>{
    loadProducts(currentPage, currentFilter);
})