document.addEventListener("DOMContentLoaded", () => {

    function formatTime(ms) {
        const sec = Math.floor(ms / 1000);
        const h = Math.floor(sec / 3600);
        const m = Math.floor((sec % 3600) / 60);
        const s = sec % 60;

        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    }

    function updateBidTimers() {
        const timers = document.querySelectorAll(".timer-countdown");

        timers.forEach(timer => {
            const startISO = timer.dataset.start;
            const durationMin = parseInt(timer.dataset.duration);

            if (!startISO || !durationMin) return;

            const start = new Date(startISO).getTime();
            const end = start + durationMin * 60 * 1000;
            const now = Date.now();

            if (now < start) {
                timer.textContent = `Começa em ${formatTime(start - now)}`;
                timer.style.color = "#007bff";
            }
            else if (now <= end) {
                timer.textContent = `Restam ${formatTime(end - now)}`;
                timer.style.color = "#28a745";
            }
            else {
                timer.textContent = "Encerrado";
                timer.style.color = "#dc3545";
            }
        });
    }

    updateBidTimers();
    setInterval(updateBidTimers, 1000);
});
