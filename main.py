import re
from datetime import datetime
import geoip2.database
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Configuration
GEOIP_DB_PATH = "GeoLite2-City.mmdb"
LOG_PATH = "access.log"

# Regular expression to parse the logs
LOG_PATTERN = re.compile(
    r'(?P<datetime>[\d\-]+\s[\d:,]+)\s-\sINFO\s-\s(?P<ip>\[?[^\]]+\]?):\d+:0\s-\s"GET\s(?P<url>[^\s]+)\sHTTP/1\.1"\s(?P<status>\d{3})'
)

# Class to store and analyze log data
class LogAnalyzer:
    def __init__(self, log_path):
        self.log_path = log_path
        self.visits = []
        self.by_ip = {}
        self.content_hits = {}
        self.status_counts = {}
        self.geoip_reader = geoip2.database.Reader(GEOIP_DB_PATH)
    
    def parse_logs(self):
        self.visits = []
        self.by_ip = {}
        self.content_hits = {}
        self.status_counts = {}
        
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
                    
                    if ip not in self.by_ip:
                        self.by_ip[ip] = []
                    self.by_ip[ip].append((dt, url, status))
                    
                    self.content_hits[url] = self.content_hits.get(url, 0) + 1
                    self.status_counts[status] = self.status_counts.get(status, 0) + 1
    
    def get_geographic_data(self):
        locations = []
        seen = set()
        
        for ip in self.by_ip:
            if ip in seen or ":" in ip:
                continue
            
            try:
                response = self.geoip_reader.city(ip)
                city = response.city.name or "Unknown"
                country = response.country.name or "Unknown"
                lat = float(response.location.latitude) if response.location.latitude else 0
                lon = float(response.location.longitude) if response.location.longitude else 0
                
                if lat != 0 and lon != 0:
                    locations.append({
                        'ip': ip,
                        'city': city,
                        'country': country,
                        'lat': lat,
                        'lon': lon,
                        'visits': len(self.by_ip[ip])
                    })
                    seen.add(ip)
            except Exception:
                pass
        
        return locations
    
    def get_user_journey(self):
        journeys = []
        for ip, visits in list(self.by_ip.items())[:5]:  # Top 5 IPs
            journey = {
                'ip': ip,
                'visits': [{'datetime': str(visit[0]), 'url': visit[1], 'status': visit[2]} 
                          for visit in sorted(visits)]
            }
            journeys.append(journey)
        return journeys
    
    def get_content_stats(self):
        sorted_content = sorted(self.content_hits.items(), key=lambda x: x[1], reverse=True)
        return sorted_content[:10]  # Top 10
    
    def get_traffic_trends(self):
        per_hour = {}
        for dt, _, _, _ in self.visits:
            hour = dt.replace(minute=0, second=0, microsecond=0)
            hour_str = hour.strftime("%Y-%m-%d %H:00")
            per_hour[hour_str] = per_hour.get(hour_str, 0) + 1
        
        return sorted(per_hour.items())

# FastAPI App
app = FastAPI(title="Log Analyzer Dashboard")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize analyzer
analyzer = LogAnalyzer(LOG_PATH)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    analyzer.parse_logs()
    
    context = {
        "request": request,
        "locations": analyzer.get_geographic_data(),
        "user_journeys": analyzer.get_user_journey(),
        "content_stats": analyzer.get_content_stats(),
        "traffic_trends": analyzer.get_traffic_trends(),
        "status_counts": analyzer.status_counts,
        "total_visits": len(analyzer.visits),
        "unique_ips": len(analyzer.by_ip)
    }
    
    return templates.TemplateResponse("index.html", context)

@app.get("/api/locations")
async def get_locations():
    analyzer.parse_logs()
    return {"locations": analyzer.get_geographic_data()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)