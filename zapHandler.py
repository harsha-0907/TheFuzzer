from zapv2 import ZAPv2
import time

class ZapScanner:
    def __init__(self):
        self.apiKey = "ept0tu3lgmr5t78k0ck536i765"
        self.zap_url = "http://127.0.0.1:8080"
        self.zap = ZAPv2(apikey=self.apiKey, proxies={'http': self.zap_url, 'https': self.zap_url})
        self.activeScans = dict()

    def start_active_scan(self, url):
        try:
            scan_id = self.zap.ascan.scan(url)
            if scan_id:
                return scan_id
            else:
                print(f"Failed to start active scan for {url}")
                return None
        except Exception as e:
            print(f"Error starting active scan for {url}: {e}")
            return None

    def add_url(self, url):
        try:
            self.zap.core.access_url(url)
            return True
        except Exception as e:
            print(f"Exception occurred while adding URL {url}: {e}")
            return False

    def monitor_scan(self, scan_id):
        try:
            while int(self.zap.ascan.status(scan_id)) < 100:
                time.sleep(2)
        except Exception as e:
            print(f"Error monitoring scan {scan_id}: {e}")

    def get_vulnerabilities(self, url):
        alerts = self.zap.alert.alerts(baseurl=url)
        add_alerts = []
        if alerts:
            for alert in alerts:
                add_alerts.append(f"{alert['alert']}")
        else:
            print(f"No vulnerabilities found for {url}")
        return add_alerts

    def scan_urls(self, urls: list):
        """Scan each URL and return a list of vulnerabilities."""
        all_alerts = []
        for url in urls:
            if self.add_url(url):
                scan_id = self.start_active_scan(url)
                if scan_id:
                    self.monitor_scan(scan_id)
                    alerts = self.get_vulnerabilities(url)
                    all_alerts.append({url: alerts})
                else:
                    print(f"Scan could not be started for {url}")
            else:
                print(f"URL could not be added: {url}")
        return all_alerts

