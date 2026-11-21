"""Fetch hourly PM10 and PM2.5 for Kraków from the GIOŚ API and save them for the web page.

Run by .github/workflows/fetch.yml every hour. Writes:
  data/krakow.json   last 72 hours per station (what the page reads)
  data/history.json  hourly values per station, kept for 60 days (for the hour-of-day pattern)
GIOŚ API: https://api.gios.gov.pl/pjp-api/ (v1). Times are Polish local time as published.
"""
import json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.gios.gov.pl/pjp-api/v1/rest"
STATIONS = {400: "Aleja Krasińskiego", 401: "ul. Bujaka", 402: "ul. Bulwarowa", 10123: "ul. Złoty Róg", 10139: "Os. Piastów",
            10447: "Os. Wadów", 11303: "Os. Swoszowice", 16896: "ul. Kamieńskiego", 20367: "ul. Półłanki"}
KEEP_DAYS = 60
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "smog-planner (github.com/costasxeras-stack/smog-planner)", "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            print(f"{e.code} {url}", file=sys.stderr)
            if 400 <= e.code < 500:
                return None
            time.sleep(3 * (i + 1))
            continue
        except Exception as e:  # noqa: BLE001
            print(f"retry {i + 1} {url}: {e}", file=sys.stderr)
            time.sleep(3 * (i + 1))
    return None


def series(sensor_id):
    out = {}
    for page in range(0, 4):
        j = get(f"{API}/data/getData/{sensor_id}?size=100&page={page}")
        if not j and page == 0:
            j = get(f"{API}/data/getData/{sensor_id}")  # some sensors reject paging parameters
            if j:
                page = 99
        if not j:
            break
        rows = j.get("Lista danych pomiarowych") or []
        for r in rows:
            v = r.get("Wartość")
            if v is not None:
                out[r["Data"][:16]] = round(float(v), 1)
        if len(rows) < 100 or page == 99:
            break
    return out


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = {"updated": now, "source": "GIOŚ, Państwowy Monitoring Środowiska", "stations": []}
    for sid, name in STATIONS.items():
        sensors = get(f"{API}/station/sensors/{sid}") or {}
        st = {"id": sid, "name": name, "pm10": {}, "pm25": {}}
        for s in sensors.get("Lista stanowisk pomiarowych dla podanej stacji", []):
            code = s.get("Wskaźnik - kod")
            if code == "PM10":
                st["pm10"] = series(s["Identyfikator stanowiska"])
            elif code == "PM2.5":
                st["pm25"] = series(s["Identyfikator stanowiska"])
        result["stations"].append(st)
    have = sum(len(s["pm10"]) + len(s["pm25"]) for s in result["stations"])
    if have == 0:
        print("No data from GIOŚ. Keeping the previous files.", file=sys.stderr)
        sys.exit(1)
    # last 72 hours for the page
    latest = max(k for s in result["stations"] for p in ("pm10", "pm25") for k in s[p])
    cutoff = (datetime.strptime(latest, "%Y-%m-%d %H:%M") - timedelta(hours=72)).strftime("%Y-%m-%d %H:%M")
    page = {"updated": now, "latest": latest, "source": result["source"], "stations": [
        {"id": s["id"], "name": s["name"], **{p: sorted([k, v] for k, v in s[p].items() if k > cutoff) for p in ("pm10", "pm25")}} for s in result["stations"]]}
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "krakow.json"), "w", encoding="utf-8") as f:
        json.dump(page, f, ensure_ascii=False, separators=(",", ":"))
    # history, merged and trimmed
    hp = os.path.join(DATA, "history.json")
    hist = {}
    if os.path.exists(hp):
        with open(hp, encoding="utf-8") as f:
            hist = json.load(f).get("stations", {})
    keep = (datetime.strptime(latest, "%Y-%m-%d %H:%M") - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d %H:%M")
    for s in result["stations"]:
        h = hist.setdefault(str(s["id"]), {"pm10": {}, "pm25": {}})
        for p in ("pm10", "pm25"):
            h[p].update(s[p])
            h[p] = {k: v for k, v in sorted(h[p].items()) if k > keep}
    with open(hp, "w", encoding="utf-8") as f:
        json.dump({"updated": now, "keep_days": KEEP_DAYS, "stations": hist}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK {have} values, latest {latest}")


if __name__ == "__main__":
    main()
