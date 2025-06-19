# 🌐 Web Access Log Analyzer for Werevi

A Python script to analyze web access logs and extract meaningful insights like:

- 🧭 User Journey Analysis  
- 🔍 Search Engine Visibility  
- 💡 Engagement with Core Features  
- 🌍 Geographic Insights (via IP)  
- 📌 Interest in Specific Content  
- 📈 Website Traffic Trends  

---

## 📁 Sample Input Format

Your `access.log` file must have lines like:

```

2025-06-14 17:47:34,797 - INFO - 190.158.28.5:10242:0 - "GET / HTTP/1.1" 200
2025-06-16 12:33:29,584 - INFO - 66.249.66.6:58625:0 - "GET /robots.txt HTTP/1.1" 404

````

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/werevi/log-analyzer.git
cd log-analyzer
````

### 2. Install Dependencies

```bash
pip install geoip2
```

### 3. Download IP Geolocation Database
#### ✅ Recommended: DB-IP (Free)


	wget -O dbip-city-lite.mmdb.gz https://download.db-ip.com/free/dbip-city-lite-$(date +%Y-%m).mmdb.gz
	gunzip dbip-city-lite.mmdb.gz

```bash
# Download current month (e.g., June 2025)
wget -O dbip-city-lite.mmdb.gz https://download.db-ip.com/free/dbip-city-lite-$(date +%Y-%m).mmdb.gz
gunzip dbip-city-lite.mmdb.gz
```

Then place `dbip-city-lite.mmdb` in the same directory and update the script path:

```python
GEOIP_DB_PATH = "dbip-city-lite.mmdb"
```

---

## 🛠️ Configuration

Update these variables in the script:

```python
GEOIP_DB_PATH = "dbip-city-lite.mmdb"  # or GeoLite2-City.mmdb
LOG_PATH = "access.log"                # your log file path
```

---

## ▶️ Usage

Run the analyzer:

```bash
python log_analyzer.py
```

It will output:

* 📌 Top accessed URLs
* 🌍 IP location data (city & country)
* 💡 Hits to core JS features
* 📈 Traffic by hour
* 🔍 Bot/scraper activity
* 🧭 Example user journeys

---

## 📦 Output Example

```
🧭 User Journey Samples
IP: 190.158.28.5
  2025-06-14 17:47:34 - / [200]
  2025-06-14 17:47:35 - /static/img/background_logo_figure.webp [200]

🌍 Geographic Insights by IP
190.158.28.5 → Bogotá, Colombia

📈 Traffic Trends (by hour)
2025-06-14 17:00:00 → 3 hits
```

---

## 📚 Dependencies

* Python 3.7+
* `geoip2`
* MMDB geolocation file from [https://db-ip.com/db/download](https://db-ip.com/db/download) or [https://dev.maxmind.com/geoip](https://dev.maxmind.com/geoip)

---

## 🧠 Insights You Can Extract

| Insight                      | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| **User Journey**             | Pages accessed per IP                           |
| **Search Engine Visibility** | IPs that behave like crawlers (Googlebot, Bing) |
| **Core Features**            | Access to `/static/js/...` files                |
| **Geo Insights**             | Approx. city & country of users                 |
| **Content Popularity**       | Most frequently accessed resources              |
| **Traffic Trends**           | Activity over time by hour                      |

