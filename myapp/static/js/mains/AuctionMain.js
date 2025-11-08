document.addEventListener('DOMContentLoaded', function () {
    const mainPhoto = document.getElementById('main-photo');
    const thumbnails = document.querySelectorAll('.thumb');

    if (!sessionStorage.getItem("noScroll")) {
        window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
        sessionStorage.removeItem("noScroll");
    }

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function () {
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            mainPhoto.src = this.getAttribute('src');
        });
    });

    const bidButton = document.querySelector('.submit-bid-btn');
    const bidInput = document.getElementById('bid-amount');
    const currentPriceDisplay = document.getElementById('current-price');
    const timeLeftDisplay = document.getElementById('time-left');

    bidButton.addEventListener('click', function () {
        if (!window.user.logged) {
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

        if (window.user.logged.wallet < newBid)
            showNotification('error', "Lance Inválidado. Saldo Insuficiente")

        bidInput.value = '';

        socket.emit('emit_bid', {
            value: newBid
        });

    });

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
    if (window.user.logged) {
        if (window.user.logged) {
            if (document.getElementById("winner-user").innerHTML === window.user.username) {
                document.getElementById("dlt-btn").style.display = "inline-block";
            }
        }
    }

    document.getElementById("dlt-btn").addEventListener("click", async () => {
        if (!window.user.logged) {
            showNotification('error', `Você nao esta logado`);
            return;
        }
        try {
            const response = await fetch(`/del/bid/${window.product_id}`, {
                method: "DELETE",
            });

            const data = await response.json();

            if (response.ok) {
                showNotification('bid', `Lance(s) retirado(s)`);
            } else {
                showNotification('error', `Não foi possivel retirar seu(s) lance(s)`);
            }
        } catch (err) {
            showNotification('error', `Não foi possivel retirar seu(s) lance(s)`);
        }
    });

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

    function showNotification(type, message) {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const notif = document.createElement('div');
        notif.className = `notification ${type}`;
        notif.textContent = message;

        container.appendChild(notif);

        const notifs = container.querySelectorAll('.notification');
        if (notifs.length > 6) {
            notifs[0].classList.add("fade-out");
            setTimeout(() => notifs[0].remove(), 300);
        }

        setTimeout(() => {
            notif.classList.add("fade-out");
            setTimeout(() => notif.remove(), 300);
        }, 5000);
    }

    function formatDateTime(dateString) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');

        const monthNames = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
        const month = monthNames[date.getMonth()];

        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        return `${day} ${month} ${year}, ${hours}:${minutes}`;
    }

    if (window.user.logged) {
        const socket = io();
        window.socket = socket;

        socket.emit('join_room', { room_id: window.roomId });

        socket.on('server_content', (data) => {
            const response = data.response;
            if (!response) return;

            switch (response.type) {
                case 'entry':
                    showNotification('join', `${response.username} entrou na sala!`);
                    break;
                case 'error':
                    const errors = {
                        101: "Informações faltantes",
                        102: "Produto invalido",
                        103: "Você não tem dinheiro suficiente",
                        104: "Lance menor que o valor minimo",
                        105: "A soma de todos os seus lances ultrapassa seu saldo",
                        106: "Erro ao processar. Tente novamente"

                    }
                    showNotification('error', `Erro: ${errors[response.error]}`);
                    break;
                case 'bid':
                    showNotification('bid', `${response.username} deu um lance de R$ ${response.value}`);
                    
                    document.getElementById("p2").innerHTML = `Seu Lance (Mínimo R$ ${(parseFloat(response.value)+1).toFixed(2).replace('.', ',')})`;
                    bidInput.placeholder = `R$ ${(parseFloat(response.value)+1).toFixed(2).replace('.', ',')}`;
                    currentPriceDisplay.textContent = `R$ ${parseFloat(response.value).toFixed(2).replace('.', ',')}`;
                    document.getElementById("p3").innerHTML = `Lance Atual: (
                        <a id="winner-user" style="margin-left:1px;margin-right:1px;" target="_blank" href="/profile/${response.username}">${response.username}</a>
                        )
                        <button class="delete-btn" id="dlt-btn" style="display: none; marin-left:4px">
                            retirar lance(s)
                        </button>`
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

                    if (window.user.logged) {
                        if (document.getElementById("winner-user").innerHTML === window.user.username) {
                            document.getElementById("dlt-btn").style.display = "inline-block";
                        }

                    }

                    break;
                case 'delete':
                    sessionStorage.setItem("noScroll", "true");
                    location.reload();
                    break;
            }
        });
    }

});
