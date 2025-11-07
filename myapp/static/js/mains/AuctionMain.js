document.addEventListener('DOMContentLoaded', function() {
    // === 1. GALERIA DE FOTOS ===
    const mainPhoto = document.getElementById('main-photo');
    const thumbnails = document.querySelectorAll('.thumb');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            mainPhoto.src = this.getAttribute('src');
        });
    });

    // === 2. LANCE PRINCIPAL ===
    const bidButton = document.querySelector('.submit-bid-btn');
    const bidInput = document.getElementById('bid-amount');
    const currentPriceDisplay = document.getElementById('current-price');
    const timeLeftDisplay = document.getElementById('time-left');

    bidButton.addEventListener('click', function() {
        if (!window.user){
            document.getElementById("loginModal").style.display = "flex";
            setTimeout(() => document.getElementById("loginModal").classList.add("show"), 10);
            return;
        }
        const newBid = parseFloat(bidInput.value.replace(',', '.'));
        const currentPrice = parseFloat(currentPriceDisplay.textContent.replace('R$ ', '').replace(',', '.'));
        if (isNaN(newBid) || newBid < currentPrice) {
            showNotification('error', `Lance inválido. Deve ser de pelo menos R$ ${(currentPrice).toFixed(2).replace('.', ',')}.`);
            return;
        }

        if(window.user.wallet < newBid)
            showNotification('error', "Lance Inválidado. Saldo Insuficiente")

        bidInput.value = '';

        // Emitir o lance via SocketIO
        console.log("foi::::")
        socket.emit('emit_bid', {
            value: newBid
        });
        
    });

    // === 3. FUNÇÃO GERAL DE CRONÔMETRO ===
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

    function setupTimer(element, relatedButton) {
        const startTime = new Date(element.dataset.start).getTime();
        const durationMinutes = parseFloat(element.dataset.duration);
        const durationMs = durationMinutes * 60 * 1000;
        const endTime = startTime + durationMs;
        const timerText = element.querySelector('.timer-text') || element;

        function updateTimer() {
            const now = new Date().getTime();
            if (now < startTime) {
                const diff = startTime - now;
                timerText.textContent = `Começa em ${formatTime(diff)}`;
                timerText.style.color = "#007bff";
                if (relatedButton) {
                    relatedButton.disabled = true;
                    relatedButton.textContent = "AGUARDANDO";
                }
            } else if (now >= startTime && now <= endTime) {
                const diff = endTime - now;
                timerText.textContent = `Tempo restante: ${formatTime(diff)}`;
                timerText.style.color = "#28a745";
                if (relatedButton) {
                    relatedButton.disabled = false;
                    relatedButton.textContent = "DAR LANCE";
                }
            } else {
                timerText.textContent = "ENCERRADO";
                timerText.style.color = "#dc3545";
                if (relatedButton) {
                    relatedButton.disabled = true;
                    relatedButton.textContent = "ENCERRADO";
                }
                clearInterval(interval);
            }
        }

        updateTimer();
        const interval = setInterval(updateTimer, 1000);
    }

    if (timeLeftDisplay) setupTimer(timeLeftDisplay, bidButton);

    const recommendedTimers = document.querySelectorAll('.recommended-timer');
    recommendedTimers.forEach(timer => {
        const button = timer.closest('.product-card').querySelector('.btn-bid');
        setupTimer(timer, button);
    });

    // === 4. FUNÇÃO DE POP-UP ===
    function showNotification(type, message) {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const notif = document.createElement('div');
        notif.className = `notification ${type}`;
        notif.textContent = message;

        // Adiciona a nova notificação no final (parte de baixo)
        container.appendChild(notif);

        // Se houver mais de 5 notificações, remove a mais antiga (a primeira)
        const notifs = container.querySelectorAll('.notification');
        if (notifs.length > 6) {
            notifs[0].classList.add("fade-out");
            setTimeout(() => notifs[0].remove(), 300);
        }

        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            notif.classList.add("fade-out");
            setTimeout(() => notif.remove(), 300);
        }, 5000);
    }

    function formatDateTime(dateString) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');

        // Mês abreviado em português (ou inglês, se preferir)
        const monthNames = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
        const month = monthNames[date.getMonth()];

        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        return `${day} ${month} ${year}, ${hours}:${minutes}`;
    }



    // === 5. SOCKETIO INTEGRATION ===
    if (window.user) {
        const socket = io();
        window.socket = socket;

        // Entrar na sala (exemplo)
        console.log("join:::")
        socket.emit('join_room', { room_id: window.roomId });

        socket.on('server_content', (data) => {
            const response = data.response;
            if (!response) return;

            switch(response.type) {
                case 'entry':
                    showNotification('join', `${response.username} entrou na sala!`);
                    break;
                case 'error':
                    showNotification('error', `Erro: ${response.error}`);
                    break;
                case 'bid':
                    showNotification('bid', `${response.username} deu um lance de R$ ${response.value}`);
                    // Atualiza o preço atual
                    document.getElementById("p2").innerHTML = `Seu Lance (Mínimo R$ ${parseFloat(response.value).toFixed(2).replace('.', ',')})`;
                    bidInput.placeholder = `R$ ${parseFloat(response.value).toFixed(2).replace('.', ',')}`;
                    currentPriceDisplay.textContent = `R$ ${parseFloat(response.value).toFixed(2).replace('.', ',')}`;
                    document.getElementById("p3").innerHTML = `Lance Atual: (<a target="_blank" href="/profile/${response.username}">${ response.username })</a>`
                    document.getElementById("p4").innerHTML = `
                    <li class="bid-entry">
                        <span class="bidder"><a href="/profile/${response.username}">
                            ${response.username}
                        </a></span>
                        <span class="bid-value">R$ ${response.value.toFixed(2).replace('.', ',')}</span>
                        <span class="bid-time"> ${formatDateTime(response.datetime)}</span>
                    </li>
                    ` + document.getElementById("p4").innerHTML;
                    document.getElementById("p5").innerHTML = "";
                    break;
            }
        });
    }

});
