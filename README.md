# 🛒 Inventory Bot

A modular, real-time inventory tracking bot with a built-in web UI. Originally built for monitoring online product restocks, this tool can now be configured to track any set of URLs and notify users when items come back in stock.

## 🚀 Features

- ✅ Periodic checking of product URLs
- 🖥️ Real-time web dashboard (Flask-based)
- 🔄 Auto-refresh via Server-Sent Events (no page reloads)
- 🔔 Optional Discord webhook alerts
- 🧠 Intelligent throttling & cooldown system
- 👤 Manual override for individual rows (mark out of stock)
- 📦 Caching and automatic expiry of old stock data
- 📊 Configurable per-domain cooldowns, intervals, and proxies
- 🔐 Admin panel for live config editing

---

## 🧰 Requirements

- Python 3.10+
- Google Chrome
- [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- ChromeDriver installed and on your PATH

Install dependencies:  
``` pip install -r requirements.txt ```

## ⚙️ Configuration

All configuration is handled via data/config.json.  
Example structure:  
```
{
  "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL",
  "discord_user_id": "YOUR_DISCORD_USER_ID",
  "use_proxies": false,
  "alert_interval": 3600,
  "check_interval": 900,
  "cooldowns": {
    "example": 1800
  },
  "urls": {
    "example": [
      "https://www.example.com/product-1",
      "https://www.example.com/product-2"
    ]
  }
}
```
🛠️ All URLs and webhook values must be updated to match your use case.

## 🖥️ Web Interface

Launch the web UI with:  
``` python ui_server.py ```

Then open [http://localhost:5000](http://localhost:5000) in your browser. The interface provides:

- A live-updating table of in-stock products
- Last and next check times
- Manual override buttons
- An admin panel at /admin for editing the config live

## 🔄 Running the Checker
To start the background checking loop:  
``` python main.py  ```  
This will continually run stock checks and update the cache on disk.

## 📁 Project Structure
```
.
├── checker/               # Core checking logic
│   ├── alert.py           # Performs the main check logic
│   ├── cache_manager.py   # Tracks current stock
│   ├── cooldown_manager.py
│   ├── notifier.py        # Sends Discord alerts
│   └── ...
├── data/
│   ├── config.json        # Main config file (edit this!)
│   └── in_stock_cache.json
├── ui/
│   ├── templates/         # Jinja2 HTML templates
│   └── static/
│       ├── js/            # Modular frontend JS
│       └── css/
├── main.py                # The main check loop
├── ui_server.py           # Flask app for the UI
└── requirements.txt
```
## 🔐 Notes

- You can mark items out of stock manually using the trash icon.
- Expired items will be pruned automatically after alert_interval.
- If you manually alter or delete the cache/config files, restart both the server and UI.
- If CAPTCHA is detected, that domain will be automatically throttled for a period.

## 📡 Notifications

If you provide a Discord webhook and user ID in the config, the bot will send alerts like this:
```
🚨 IN STOCK ALERT
Store: example.com
Price: $999.99
🔗 View Product: https://www.example.com/product-1
🕒 Checked at: 
```

## 🧪 Debugging

- All debug HTML and errors are saved to the debug/ folder
- Logs will print to the terminal while main.py is running
- If the bot gets stuck after a crash, it will automatically clear stale flags
