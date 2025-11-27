 
 function setupTimer(element, relatedButton) {
    const startTime = new Date(element.dataset.start).getTime();
    const durationMinutes = parseFloat(element.dataset.duration);
    const durationMs = durationMinutes * 60 * 1000;

    let endTime = startTime + durationMs;
    if (element.dataset.dynamicEndTime) {
        endTime = parseInt(element.dataset.dynamicEndTime);
    }

    function updateTimer() {
        const now = Date.now();

        if (element.dataset.dynamicEndTime) {
            endTime = parseInt(element.dataset.dynamicEndTime);
        }

        if (now < startTime) {
            const diff = startTime - now;
            element.textContent = `Começa em ${formatTime(diff)}`;
        } else if (now >= startTime && now <= endTime) {
            const diff = endTime - now;
            element.textContent = `Tempo restante: ${formatTime(diff)}`;
        } else {
            element.textContent = "ENCERRADO";
            clearInterval(interval);
        }
    }

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
}

 
 document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".timer-countdown").forEach(timer => {
        setupTimer(timer, null);
    });
});
