document.addEventListener('DOMContentLoaded', () => {

    // --- Loading Overlay ---
    const loadingOverlay = document.getElementById('loading-overlay');
    const showLoading = () => loadingOverlay?.classList.add('active');
    const hideLoading = () => loadingOverlay?.classList.remove('active');

    // --- Elementos principais ---
    const productsGrid = document.querySelector('.product-grid');
    const paginationList = document.querySelector('.pagination-list');
    const filterPriceBox = document.querySelector('.price-range-filter');
    const inputsPrice = filterPriceBox.querySelectorAll('.price-inputs input');
    const btnApplyPrice = filterPriceBox.querySelector('.btn-filter-apply');
    const btnClearFilters = document.querySelector('.btn-clear-filters');

    let currentPage = 1;
    let totalPages = 1;
    let filters = {
        category: null,
        status: null,
        price_range: null,
        name: null
    };

    // --- Renderização de produtos ---
    function renderProducts(products) {
        productsGrid.innerHTML = '';
        products.forEach(product => {
            const photoUrl = product.photo_url?.photo_url || 'https://via.placeholder.com/250x180/E0E0E0/333333?text=Sem+Imagem';
            const card = `
                <div class="product-card">
                    <div class="product-image" style="background-image: url('${ product.photo_url}');"></div>
                    ${product.badge ? `<span class="badge ${product.badge_class || ''}">${product.badge}</span>` : ''}
                    <h3>${product.product_name}</h3>
                    <p class="price">R$ ${product.min_bid || '0,00'}</p>
                    <p class="time-left"><i class="far fa-clock"></i> Tempo: ${product.time_left || '--:--:--'}</p>
                    <a href="/auction/${product.room}"><button class="btn-bid" >DAR LANCE</button></a>
                </div>
            `;
            productsGrid.insertAdjacentHTML('beforeend', card);
        });
    }

    // --- Paginação ---
    function renderPagination(current, total) {
        paginationList.innerHTML = `
            <li class="page-item prev ${current === 1 ? 'disabled' : ''}">
                <a href="#" class="page-link"><i class="fas fa-angle-left"></i></a>
            </li>
        `;
        for (let i = 1; i <= total; i++) {
            if (i === 1 || i === total || (i >= current - 2 && i <= current + 2)) {
                paginationList.innerHTML += `
                    <li class="page-item ${i === current ? 'active' : ''}">
                        <a href="#" class="page-link">${i}</a>
                    </li>
                `;
            } else if (i === 2 && current > 4) {
                paginationList.innerHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            } else if (i === total - 1 && current < total - 3) {
                paginationList.innerHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }
        paginationList.innerHTML += `
            <li class="page-item next ${current === total ? 'disabled' : ''}">
                <a href="#" class="page-link"><i class="fas fa-angle-right"></i></a>
            </li>
        `;
    }

    // --- Carrega produtos via AJAX ---
    function loadProducts(page = 1) {
        showLoading();
        let url = window.paginate_args;
        if( page > 1){
            url = `/paginate/auction/${page}?`
        }

        if (filters.category) url += `category=${filters.category}&`;
        if (filters.status) url += `status=${filters.status}&`;
        if (filters.price_range) url += `price_range=${filters.price_range}&`;
        if (filters.name) url += `name=${filters.name}&`;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                renderProducts(data.products);
                currentPage = data.current_page;
                totalPages = data.total_pages;
                renderPagination(currentPage, totalPages);
                document.querySelector('.sort-and-count p').textContent =
                    `Mostrando página ${currentPage} de ${totalPages}`;
                hideLoading();
            })
            .catch(err => {
                console.error('Erro ao carregar produtos:', err);
                hideLoading();
            });
        window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    // --- Paginação (cliques) ---
    paginationList.addEventListener('click', e => {
        e.preventDefault();
        const target = e.target.closest('.page-link');
        if (!target || target.parentElement.classList.contains('disabled')) return;

        let page = target.textContent.trim();
        if (page === '…') return;

        if (target.parentElement.classList.contains('prev')) page = currentPage - 1;
        if (target.parentElement.classList.contains('next')) page = currentPage + 1;

        loadProducts(Number(page));
        window.scrollTo({ top: 100, behavior: 'smooth' });
    });

    // --- Filtros por link ---
    document.querySelectorAll('[data-type][data-val]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();

            const type = link.dataset.type;
            const val = link.dataset.val;

            // Atualiza filtros
            filters[type] = val;

            // Marca visualmente o link ativo
            document.querySelectorAll(`[data-type="${type}"]`).forEach(l => l.classList.remove('active-filter'));
            link.classList.add('active-filter');

            // Atualiza apenas o parâmetro da URL (sem perder os outros)
            const url = new URL(window.location.href);
            url.searchParams.set(type, val);

            // Atualiza sem recarregar a página
            history.pushState({}, '', url);
            loadProducts(1);
        });
    });

    // --- Filtro de preço ---
    btnApplyPrice.addEventListener('click', () => {
        const min = inputsPrice[0].value.trim();
        const max = inputsPrice[1].value.trim();
        if (!min || !max) {
            alert('Por favor, preencha ambos os valores.');
            return;
        }

        filters.price_range = `${min}-${max}`;
        const url = new URL(window.location.href);
        url.searchParams.set('price_range', filters.price_range);

        history.pushState({}, '', url);
        loadProducts(1);
    });

    // --- Limpar filtros ---

    // --- Inicializa ---
    loadProducts(1);
});
