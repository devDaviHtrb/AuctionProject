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
        const newBid = parseFloat(bidInput.value.replace(',', '.'));
        const currentPrice = parseFloat(currentPriceDisplay.textContent.replace('R$ ', '').replace('.', '').replace(',', '.'));
        const minIncrement = 50.00;

        if (isNaN(newBid) || newBid < (currentPrice + minIncrement)) {
            alert(`Lance inválido. Seu lance deve ser de pelo menos R$ ${(currentPrice + minIncrement).toFixed(2).replace('.', ',')}.`);
            return;
        }

        currentPriceDisplay.textContent = `R$ ${newBid.toFixed(2).replace('.', ',')}`;
        bidInput.value = '';
        alert(`Seu lance de R$ ${newBid.toFixed(2).replace('.', ',')} foi registrado!`);
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

    // === 4. CRONÔMETRO DO LEILÃO PRINCIPAL ===
    if (timeLeftDisplay) setupTimer(timeLeftDisplay, bidButton);

    // === 5. CRONÔMETROS DOS RECOMENDADOS ===
    const recommendedTimers = document.querySelectorAll('.recommended-timer');
    recommendedTimers.forEach(timer => {
        const button = timer.closest('.product-card').querySelector('.btn-bid');
        setupTimer(timer, button);
    });
});