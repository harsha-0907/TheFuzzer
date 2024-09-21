#!/bin/python3

from packages import *
from initProgram import *

def dns_lookup(domain="", attempts = 0):
	"""
		Here the domain name will be checked for all the records. If any records are present, then it will return the data else. It will return an empty list
	"""
	try:
		if domain == "":
			raise dns.resolver
		ips = dns_resolver.resolve(domain, 'A')
		ipaddresses = [str(ip) for ip in ips]
		return ipaddresses
		
	except (dns_resolver.NXDOMAIN, dns_resolver.NoAnswer):
		return []
	except dns_resolver.Timeout:
		if attempts > 3:
			return []
		else:
			return dns_lookup(domain, attempts+1)
	except Exception as e:
		return []


domain = "google.com"
res = dns_lookup(domain)
json_data = readJSONData()

res = updateJSONData({'ip-addresses': res})

dumpJSONData(res)
