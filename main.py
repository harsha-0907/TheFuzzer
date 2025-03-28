#!/bin/bash

# This program will be used tas the flow-control of the program
# This program will be running various programs.


from packages import *
from initProgram import *
from dnsresolution import *
from subDomainEnum import SubDomainEnumerator
from grawler.crawler import Crawler
from serviceEnumeration import *
import json
import time
from zapHandler import ZapScanner


class Application():
	def __init__(self, domain_name):
		self.info = dict()
		self.info['domain_name'] = domain_name
		self.info['domain_ip'] = dns_lookup(self.info['domain_name'])
		if self.info['domain_ip'] == []:
			# The domain name is invalid or some internal error
			# We will stop if the resume is False
			self.resume = False
		else:
			self.resume = True
			dir_path = createDirectory(domain_name) + '/'
			self.info['directory-path'] = dir_path
			self.info['variables-path'] = dir_path + 'variables.json'
			dumpJSONData(self.info, dir_path+'variables.json')

	def dumpData(self):
		"""To update the json in the variables.json file"""
		try:
			dumpJSONData(self.info, self.info['variables-path'])
			return True
		except Exception as e:
			return False
	
	def updateJSONData(self, data):
		"""To update the self.info with any new data"""
		for i in data:
			self.info[i] = data[i]
	
	def startup():
		""" Here the process of sub-domain enum and service-enum must be completed.
			The only part that should remain will be using the Crawler & ZAP testing that will be done in the main method """
			
			

class VulnScanner:
	def __init__(self, domain):
		self.domain_name = domain
	
	def startup(self):
		""" Here the process of sub-domain enum and service-enum must be completed.
			The only part that should remain will be using the Crawler & ZAP testing that will be done in the main method """
		try:
			self.app = Application(self.domain_name)
			if not  self.app.resume:
				print("Domain Not Found")
				exit()
			# Starting the sub-domain enum
			print("Domain Found")
			print("Starting Sub-Domain Enum")
			subdomains = SubDomainEnumerator(self.domain_name).fetchSubDomains()
			self.subdomains = subdomains
			print("Sub-Domain Enumeration is Complete")
			print(f"Total number of fetched Sub-domains : {len(subdomains)}")
			self.app.info['sub-domains'] = subdomains
			self.app.dumpData()
			
			# Service Enumeration begins here
					
			print("Starting Service-Version Enumeration")
			self.app.info['service-enum'] = serviceVersionEnumeration(subdomains)
			self.app.dumpData()
			print("Service Enumeration complete")

		except Exception as _e:
			print("An Error occured while starting up the scanner")
			print(f"Details of the error {_e}")
			exit()
		
	def scan(self):
		self.startup()
		# Running the crawler
		print("Crawling the sub-domains")
		self.app.info["crawled-urls"] = dict()
		for subdomain in self.subdomains:
			crawler = Crawler(domain=subdomain)
			crawled_urls = crawler.crawl()
			self.app.info["crawled-urls"][subdomain] = crawled_urls
		print("Crawler-Complete")
		# Running the scanner
		
		self.activeResults = {}
		self.scanner = ZapScanner()
		for subdomain in self.app.info["crawled-urls"]:
			# Let us cap the number of urls that are going to be tested to 5
			subdomain_urls = self.app.info["crawled-urls"][subdomain][:5]
			scanner = ZapScanner()
			scan_results = scanner.scan_urls(subdomain_urls)
			self.activeResults[subdomain] = scan_results
			print(f"Results for {subdomain} : ", scan_results, end="\n")
		
		self.app.info["scan-results"] = self.activeResults
		self.app.dumpData()
		

if __name__ == "__main__":
	try:
		scanner = VulnScanner(domain=sys.argv[1])
		results = {"scan-results": scanner.scan()}
		
		with open("scan-results.json", 'w') as file:
			file.write(json.dumps(results))
		"""
		domain_name = sys.argv[1]
		a = Application(domain_name)
		#print(a.info, a.resume)
		if not a.resume:
			print("Domain Not Found")
			exit()
		# Starting the sub-domain enum
		print("Domain Found")
		print("Starting Sub-Domain Enum")
		subdomains = SubDomainEnumerator(domain_name).fetchSubDomains()
		print(subdomains)
		print("Sub-Domain Enumeration Complete")
		a.info['sub-domains'] = subdomains
		a.dumpData()
		# Service Enumeration using nmap
		print("Starting Service-Version Enumeration")
		a.info['service-enum'] = serviceVersionEnumeration(subdomains)
		a.dumpData()
		print("Starting Active Scan... this might take a lot of time")
		scanner = ZapScanner()
		scans = dict()
		for subdomain in subdomains:
			scanId = scanner.activeScan(subdomain)
			scans[subdomain] = scanId
		
		# We wait until all the scans are completed
		while len(scanner.activeScans) > 0:
			scanner.scanProgress()	# To check if the scan is completed
			time.sleep(5)
		
		results = dict()
		for domain in subdomains:
			results[domain] = dict()
			domain_alerts = scanner.core.get_alerts(baseurl=target, start=0, count=5000)
			blacklist = [1,2]
			for alert in domain_alerts:
				plugin_id = alert['pluginId']
				if plugin_id in blacklist:
					continue
				results[domain] = {"pluginId": plugin_id, "risk": alert["risk"], "url": alert["url"], "description": alert["description"]}

		with open("results.json", 'w', encodin="utf-8") as file:
			file.write(json.sump(results))
		"""		
	except IndexError:
		if len(sys.argv) < 2:
			print("Domain Name is Empty!!!")
		else:
			print("Error")
	except Exception as e:
		print("An Error has occured", e)
