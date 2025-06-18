import asyncio
import json
import checker.shared_state as state
import threading
import time
from flask import Flask, Response, render_template, redirect, url_for, request, jsonify
from checker.cache_manager import cache_manager
from checker.run_schedule import run_schedule
from checker.config_manager import ConfigManager
from checker.runner import run_check_now
from pathlib import Path

app = Flask(__name__, template_folder="ui/templates", static_folder="ui/static")

@app.template_filter('timestamp_to_str')
def timestamp_to_str_filter(ts):
    from time import strftime, localtime
    return strftime('%Y-%m-%d %H:%M:%S', localtime(ts))

@app.template_filter('time_remaining')
def time_remaining_filter(ts):
    from time import time
    config = ConfigManager.get()
    ttl = config.get("alert_interval", 3600)
    remaining = max(0, int(ts + ttl - time()))
    mins, secs = divmod(remaining, 60)
    return f"{mins}m {secs}s"

@app.route('/clear-cache')
def clear_cache():
    cache_manager.clear()
    return redirect(url_for('index'))

@app.route('/stream')
def stream():
    def event_stream():
        last_sent = 0
        while True:
            time.sleep(1)
            current = max(
                run_schedule.get_last_run_time(),
                run_schedule.get_last_alert_time()
            )
            if current > last_sent:
                last_sent = current
                yield f"data: update\n\n"
    return Response(event_stream(), content_type='text/event-stream')

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

@app.route('/')
def index():
    config = ConfigManager.get()
    cache_manager.load()
    cache_manager.prune(config.get("alert_interval", 3600))
    return render_template(
        "index.html",
        stock=cache_manager.get_cache(),
        last_check=run_schedule.get_last_run_time(),
        next_check=run_schedule.load()
    )


@app.route('/api/stock/html')
def stock_table_html():
    config = ConfigManager.get()
    cache_manager.load()
    cache_manager.prune(config.get("alert_interval", 3600))
    return render_template("stock_table.html", stock=cache_manager.get_cache())

@app.route('/api/status/time')
def get_last_run_time():
    return {
        "last_run": run_schedule.get_last_run_time(),
        "next_run": run_schedule.load()
    }

@app.route('/force-check')
def force_check():
    if state.is_checking():
        return ("Already checking", 429)  # HTTP 429 Too Many Requests

    def launch():
        asyncio.run(run_check_now())

    threading.Thread(target=launch).start()
    return ("", 204)

@app.route('/api/check-status')
def check_status():
    return {"in_progress": state.is_checking()}

@app.route('/api/mark-out-of-stock/<path:url>')
def mark_out_of_stock(url):
    from urllib.parse import unquote
    decoded_url = unquote(url)
    if decoded_url in cache_manager.get_cache():
        cache_manager.set_expired(decoded_url)
    return ("", 204)

@app.route('/admin')
def admin_page():
    config = ConfigManager.get()
    return render_template("admin.html", config=config)

@app.route('/api/admin/config', methods=['GET', 'POST'])
def config_api() -> Response:
    config_path = Path("data/config.json")

    if request.method == 'GET':
        with config_path.open() as f:
            return jsonify(json.load(f))

    if request.method == 'POST':
        new_config = request.get_json()
        with config_path.open('w') as f:
            json.dump(new_config, f, indent=2)
        return Response(status=204)

    # Fallback for unsupported methods (e.g. someone sends PUT by accident)
    return Response("Method Not Allowed", status=405)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
