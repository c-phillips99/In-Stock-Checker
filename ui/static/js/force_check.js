import { showToast } from "./toast.js";
import { updateCountdown } from "./countdown.js";
import { fetchJSON } from "./utils.js";

document.getElementById("force-check-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    showToast("Forcing stock check...");

    await fetch("/force-check");

    const { next_run } = await fetchJSON("/api/status/time");

    updateCountdown(next_run);
});
