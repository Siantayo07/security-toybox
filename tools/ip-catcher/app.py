from flask import Flask, request, render_template, abort
import requests
import datetime

app = Flask(__name__)

def get_ip(request):
    return request.headers.get("X-Forwarded-For", request.remote_addr)

def lookup_ip(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        return res.json()
    except:
        return {}

def sanitize_ip(ip):
    if ip and ',' in ip:
        # Take first IP in comma-separated list
        ip = ip.split(',')[0].strip()
    if ip.startswith("::ffff:"):
        ip = ip.replace("::ffff:", "")
    return ip


def log_visitor(ip, ua, geo):
    try:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{time}] IP: {ip} | UA: {ua}\n"
        if geo:
            entry += (
                f"    City: {geo.get('city', 'N/A')} | "
                f"Country: {geo.get('country', 'N/A')} | "
                f"Org: {geo.get('org', 'N/A')} | "
                f"Coordinates: {geo.get('loc', 'N/A')}\n"
            )
        with open("visitors.log", "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Logged visitor: {ip}")
    except Exception as e:
        print(f"Error logging visitor: {e}")
        print(f"Visitor: {ip} from {geo.get('city', 'Unknown')} at {time}")


@app.route("/")
def index():
    ip = sanitize_ip(get_ip(request))
    ua = request.headers.get("User-Agent", "Unknown")
    geo = lookup_ip(ip)
    log_visitor(ip, ua, geo)
    return render_template("index.html", ip=ip, ua=ua, geo=geo)

LOG_ROUTE = "/log-ptvlwwrt"
ACCESS = "AvNlwlh9Fq"

@app.route(LOG_ROUTE)
def view_logs():
    token = request.args.get("token")
    if token != ACCESS:
        abort(403)

    try:
        with open("visitors.log", "r", encoding="utf-8") as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except FileNotFoundError:
        return "No log file found yet. Visit the main page first to create it."
    except Exception as e:
        return f"Error reading logs: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
