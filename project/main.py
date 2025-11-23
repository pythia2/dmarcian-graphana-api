from flask import Flask
from datetime import date, timedelta
import requests
import os

app = Flask(__name__)

API_TOKEN = os.environ.get('API_TOKEN', '').strip()
BASE_URL = os.environ.get('BASAE_URL', '').strip()
HEADERS = {"Authorization": API_TOKEN}
CREATE_REPORT = "detail-viewer/"
REPORT_PAYLOAD = {
    #"domains": [""],
    "start_date": "",
    "end_date": "",
    "filter_option": "n"
}

@app.route('/')
def home():
    return "<h1>Hello, World!</h1><p>The app is running.</p>"

@app.route('/api/threat-unknown')
def get_threat_unknown_chart():
    charts = get_charts()
    threat_unknown_chart = charts["timeline"]["4"]
    return threat_unknown_chart


@app.route('/api/dmarc-capable')
def get_dmarc_capable_chart():
    charts = get_charts()
    dmarc_capable_chart = charts["timeline"]["1"]
    return dmarc_capable_chart

def dmarcian_api(method, endpoint, headers, payload=None):

    try:
        response = requests.request(
            method=method,
            url=f"{BASE_URL}{endpoint}",
            json=payload,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print(f"Server Response: {response.text}")
        return None

    except Exception as err:
        print(f"Connection Error: {err}")
        return None

def get_charts():
    payload = set_date(REPORT_PAYLOAD)
    data = dmarcian_api("POST", CREATE_REPORT, HEADERS, payload)
    charts_url = data.get("_links").get("charts")
    charts_endpoint = charts_url.removeprefix(BASE_URL)
    charts = dmarcian_api("GET", charts_endpoint, HEADERS)

    return charts

def set_date(payload):
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    payload["start_date"] = str(thirty_days_ago)
    payload["end_date"] = str(today)

    return payload
