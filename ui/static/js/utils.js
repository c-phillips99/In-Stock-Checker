// Format and inject last checked timestamp
export function updateLastChecked(unixTimestamp) {
    const lastCheckedDiv = document.querySelector(".status-bar div strong").parentElement;
    const dateStr = new Date(unixTimestamp * 1000).toLocaleString();
    lastCheckedDiv.innerHTML = `<strong>Last Checked:</strong> ${dateStr}`;
}

export async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Fetch failed: ${url}`);
    return res.json();
}