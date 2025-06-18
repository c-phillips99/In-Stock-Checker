import { updateCountdown } from "./countdown.js";
import "./sse_updates.js";
import "./force_check.js";
import "./expires_timer.js";
import "./row_controls.js";

// Global error handler
window.addEventListener("error", (e) => {
    console.error("💥 Global JS error:", e.message, e.filename, e.lineno);
});

const initialNextCheck = Number(document.body.getAttribute("data-next-check"));
updateCountdown(initialNextCheck);
