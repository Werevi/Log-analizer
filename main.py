import re
from collections import defaultdict, Counter
from datetime import datetime
import geoip2.database  # pip install geoip2

# Set path to GeoLite2-City.mmdb for geo lookup (you must download this file)
GEOIP_DB_PATH = "GeoLite2-City.mmdb"

LOG_PATH = "access.log"  # Change this to your log file

# Regular expression to parse the logs
LOG_PATTERN = re.compile(
    r'(?P<datetime>[\d\-]+\s[\d:,]+)\s-\sINFO\s-\s(?P<ip>\[?[^\]]+\]?):\d+:0\s-\s"GET\s(?P<url>[^\s]+)\sHTTP/1\.1"\s(?P<status>\d{3})'
)

# Class to store and analyze log data
class LogAnalyzer:
    def __init__(self, log_path):
        self.log_path = log_path
        self.visits = []
        self.by_ip = defaultdict(list)
        self.content_hits = Counter()
        self.status_counts = Counter()
        self.geoip_reader = geoip2.database.Reader(GEOIP_DB_PATH)

    def parse_logs(self):
        with open(self.log_path, "r") as f:
            for line in f:
                match = LOG_PATTERN.search(line)
                if match:
                    data = match.groupdict()
                    dt = datetime.strptime(data['datetime'], "%Y-%m-%d %H:%M:%S,%f")
                    ip = data['ip'].strip("[]")
                    url = data['url']
                    status = int(data['status'])

                    self.visits.append((dt, ip, url, status))
                    self.by_ip[ip].append((dt, url, status))
                    self.content_hits[url] += 1
                    self.status_counts[status] += 1

    def user_journey(self):
        print("\n🧭 User Journey Samples")
        for ip, visits in list(self.by_ip.items())[:3]:
            print(f"\nIP: {ip}")
            for visit in sorted(visits):
                print(f"  {visit[0]} - {visit[1]} [{visit[2]}]")

    def search_engine_visibility(self):
        print("\n🔎 Search Engine Bots (IP & URLs)")
        for ip, visits in self.by_ip.items():
            if any("google" in url or "bot" in url or ip.startswith("66.") or ip.startswith("40.") for _, url, _ in visits):
                print(f"\nIP: {ip}")
                for dt, url, status in visits:
                    print(f"  {dt} - {url} [{status}]")

    def core_feature_engagement(self):
        print("\n💡 Engagement with Core Features")
        features = ["/static/js/quick-calculator.js", "/static/js/hero-map.js", "/static/js/traffic-map.js"]
        for f in features:
            print(f"{f} → {self.content_hits[f]} hits")

    def geographic_insights(self):
        print("\n🌍 Geographic Insights by IP")
        seen = set()
        for ip in self.by_ip:
            if ip in seen or ":" in ip:
                continue
            try:
                response = self.geoip_reader.city(ip)
                city = response.city.name or "Unknown"
                country = response.country.name or "Unknown"
                print(f"{ip} → {city}, {country}")
                seen.add(ip)
            except Exception:
                pass

    def interest_in_content(self):
        print("\n📌 Interest in Specific Content")
        top = self.content_hits.most_common(5)
        for url, count in top:
            print(f"{url} → {count} hits")

    def traffic_trends(self):
        print("\n📈 Traffic Trends (by hour)")
        per_hour = defaultdict(int)
        for dt, _, _, _ in self.visits:
            hour = dt.replace(minute=0, second=0, microsecond=0)
            per_hour[hour] += 1
        for hour in sorted(per_hour):
            print(f"{hour} → {per_hour[hour]} hits")

    def run_all(self):
        self.parse_logs()
        self.user_journey()
        self.search_engine_visibility()
        self.core_feature_engagement()
        self.geographic_insights()
        self.interest_in_content()
        self.traffic_trends()

if __name__ == "__main__":
    analyzer = LogAnalyzer(LOG_PATH)
    analyzer.run_all()

