import { showToast } from "./toast.js";
import { updateCountdown } from "./countdown.js";
import { updateLastChecked } from "./utils.js";
import { fetchJSON } from "./utils.js";

const evtSource = new EventSource("/stream");

evtSource.onmessage = async function(event) {
    if (event.data === "update") {
        const res = await fetch('/api/stock/html');
        const html = await res.text();

        const newContainer = document.createElement("tbody");
        newContainer.innerHTML = html;

        const tbody = document.getElementById("stock-table-body");
        const oldRows = Array.from(tbody.children);
        const newRows = Array.from(newContainer.children);

        for (let i = 0; i < newRows.length; i++) {
            const newRow = newRows[i];
            const oldRow = oldRows[i];

            if (!oldRow || newRow.innerHTML !== oldRow.innerHTML) {
                if (oldRow) tbody.replaceChild(newRow, oldRow);
                else tbody.appendChild(newRow);
                newRow.classList.add("updated");
                setTimeout(() => newRow.classList.remove("updated"), 1000);
            }
        }

        const { last_run, next_run } = await fetchJSON("/api/status/time");
        updateLastChecked(last_run);
        updateCountdown(next_run);

        showToast("Stock table updated!");
    }
};
