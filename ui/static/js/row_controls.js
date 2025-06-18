import { showToast } from "./toast.js";

document.addEventListener("click", async function (e) {
    if (e.target?.classList.contains("btn-trash")) {
        const url = e.target.getAttribute("data-url");
        if (!url) return;
        const encoded = encodeURIComponent(url);
        await fetch(`/api/mark-out-of-stock/${encoded}`);
        showToast("Manually marked as out of stock");

        const res = await fetch("/api/stock/html");
        const html = await res.text();

        const tbody = document.getElementById("stock-table-body");
        if (tbody) tbody.innerHTML = html;
    }
});