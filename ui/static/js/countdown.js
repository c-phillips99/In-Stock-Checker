import { fetchJSON } from "./utils.js";

let countdownInterval = null;

export function updateCountdown(targetTimestamp) {
    const timerSpan = document.getElementById("next-check-timer");

    async function update() {
        const now = Math.floor(Date.now() / 1000);
        const diff = targetTimestamp - now;
        const status = await fetchJSON("/api/check-status");
        timerSpan.classList.remove("green", "red");

        if (status.in_progress) {
            timerSpan.textContent = "Check in progress...";
        } else if (diff <= 0) {
            timerSpan.textContent = "Ready for check";
            timerSpan.classList.add("green");
        } else {
            const mins = Math.floor(diff / 60);
            const secs = diff % 60;
            timerSpan.textContent = `${mins}m ${secs}s`;
            if (diff <= 60) {
                timerSpan.classList.add("red");
            }
        }
    }

    clearInterval(countdownInterval);
    countdownInterval = setInterval(update, 1000);
    update();
}
