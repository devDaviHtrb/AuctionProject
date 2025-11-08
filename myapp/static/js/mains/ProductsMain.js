document.addEventListener('DOMContentLoaded', () => {

    const loadingOverlay = document.getElementById('loading-overlay');
    const showLoading = () => loadingOverlay?.classList.add('active');
    const hideLoading = () => loadingOverlay?.classList.remove('active');

    const productsGrid = document.querySelector('.product-grid');
    const paginationList = document.querySelector('.pagination-list');
    const filterPriceBox = document.querySelector('.price-range-filter');
    const inputsPrice = filterPriceBox.querySelectorAll('.price-inputs input');
    const btnApplyPrice = filterPriceBox.querySelector('.btn-filter-apply');
    const btnClearFilters = document.querySelector('.btn-clear-filters');
    const sortSelect = document.getElementById('sort'); // select de ordenação

    let currentPage = 1;
    let totalPages = 1;
    let filters = {
        category: null,
        status: null,
        price_range: null,
        name: null,
        sort: null 
    };

    function formatTime(ms) {
        const totalSeconds = Math.floor(ms / 1000);
        const days = Math.floor(totalSeconds / (3600 * 24));
        const hours = Math.floor((totalSeconds % (3600 * 24)) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        let parts = [];
        if (days > 0) parts.push(`${days}d`);
        if (hours > 0) parts.push(`${hours}h`);
        if (minutes > 0) parts.push(`${minutes}m`);
        parts.push(`${seconds}s`);
        return parts.join(" ");
    }

    function setupProductTimer(timerElement, startTimeISO, durationMinutes, buttonElement) {
        const startTime = new Date(startTimeISO).getTime();
        const durationMs = durationMinutes * 60 * 1000;
        const endTime = startTime + durationMs;

        function updateTimer() {
            const now = new Date().getTime();
            if (now < startTime) {
                timerElement.textContent = `Começa em ${formatTime(startTime - now)}`;
                timerElement.style.color = "#007bff";
                if (buttonElement) {
                    buttonElement.disabled = true;
                    buttonElement.textContent = "AGUARDANDO";
                }
            } else if (now >= startTime && now <= endTime) {
                timerElement.textContent = `Tempo restante: ${formatTime(endTime - now)}`;
                timerElement.style.color = "#28a745";
                if (buttonElement) {
                    buttonElement.disabled = false;
                    buttonElement.textContent = "DAR LANCE";
                }
            } else {
                timerElement.textContent = "ENCERRADO";
                timerElement.style.color = "#dc3545";
                if (buttonElement) {
                    buttonElement.disabled = true;
                    buttonElement.textContent = "ENCERRADO";
                }
                clearInterval(interval);
            }
        }

        updateTimer();
        const interval = setInterval(updateTimer, 1000);
    }

    function renderProducts(products) {
        productsGrid.innerHTML = '';

        products.forEach(product => {
            const photoUrl = product.photo_url?.photo_url || 'https://via.placeholder.com/250x180/E0E0E0/333333?text=Sem+Imagem';

            const card = document.createElement('div');
            card.classList.add('product-card');
            card.innerHTML = `
                <div class="product-image" style="background-image: url('${photoUrl}');"></div>
                ${product.badge ? `<span class="badge ${product.badge_class || ''}">${product.badge}</span>` : ''}
                <h3>${product.product_name}</h3>
                <p class="price">R$ ${parseFloat(product.min_bid || 0).toFixed(2)}</p>
                <p class="time-left"><i class="far fa-clock"></i> <span class="timer-text">--:--:--</span></p>
                <a href="/auction/${product.room}"><button class="btn-bid">DAR LANCE</button></a>
            `;
            
            productsGrid.appendChild(card);

            const timerElement = card.querySelector('.timer-text');
            const buttonElement = card.querySelector('.btn-bid');
            setupProductTimer(timerElement, product.start_datetime, product.duration, buttonElement);
        });
    }

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

    function loadProducts(page = 1) {
        showLoading();
        showLoading();
        let url = page > 1 ? `/paginate/auction/${page}?` : window.paginate_args;
        if (filters.category) url += `category=${filters.category}&`;
        if (filters.status) url += `status=${filters.status}&`;
        if (filters.price_range) url += `price_range=${filters.price_range}&`;
        if (filters.name) url += `name=${filters.name}&`;
        if (filters.sort) url += `sort=${filters.sort}&`;

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
                console.error( err);
                hideLoading();
            });

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    paginationList.addEventListener('click', e => {
        e.preventDefault();
        const target = e.target.closest('.page-link');
        if (!target || target.parentElement.classList.contains('disabled')) return;

        let page = target.textContent.trim();
        if (page === '…') return;

        if (target.parentElement.classList.contains('prev')) page = currentPage - 1;
        if (target.parentElement.classList.contains('next')) page = currentPage + 1;

        loadProducts(Number(page));
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    document.querySelectorAll('[data-type][data-val]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            e.stopPropagation();

            const type = link.dataset.type;
            const val = link.dataset.val;

            filters[type] = val;

            document.querySelectorAll(`[data-type="${type}"]`).forEach(l => l.classList.remove('active-filter'));
            link.classList.add('active-filter');

            const url = new URL(window.location.href);
            url.searchParams.set(type, val);
            history.pushState({}, '', url);

            loadProducts(1);
        });
    });

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

    sortSelect.addEventListener('change', () => {
        const val = sortSelect.value;
        switch(val) {
            case "Mais Recentes": filters.sort = "recent_desc"; break;
            case "Menos Recentes": filters.sort = "recent_asc"; break; // exemplo: por tempo restante crescente
            case "Menor Preço": filters.sort = "price_asc"; break;
            case "Maior Preço": filters.sort = "price_desc"; break;
            default: filters.sort = null; break;
        }
        loadProducts(1);
    });

    loadProducts(1);
});
