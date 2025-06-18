function updateExpiresInTimers() {
    const expiresCells = document.querySelectorAll("td.expires-in");
    const now = Math.floor(Date.now() / 1000);
    const alertInterval = 3600; // You could dynamically load this from the server later

    expiresCells.forEach(cell => {
        const createdAt = parseInt(cell.getAttribute("data-timestamp"));
        const remaining = Math.max(0, createdAt + alertInterval - now);
        const mins = Math.floor(remaining / 60);
        const secs = remaining % 60;
        cell.textContent = `${mins}m ${secs}s`;
    });
}

setInterval(updateExpiresInTimers, 1000);
