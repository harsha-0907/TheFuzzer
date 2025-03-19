API_KEY = "ept0tu3lgmr5t78k0ck536i765"

from zapv2 import ZAPv2
import time

class ZapScanner:
	def __init__(self):
		self.apiKey = "ept0tu3lgmr5t78k0ck536i765"
		self.scanner = ZAPv2(apikey = self.apiKey)
		self.activeScans = dict()
		
	def activeScan(self, target: str):
		scanId = self.scanner.ascan.scan(target)
		self.activeScans[scanId] = True
		return scanId

	def scanProgress(self, scanId: str | None = None):
		if scanId in self.activeScans:
			status = int(self.scanner.ascan.status(scanId))
			if status == 100:
				del(self.scanner.activeScans[scanId])
		return 0


