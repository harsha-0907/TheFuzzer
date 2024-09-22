#!/bin/python3

from packages import *
from initProgram import *

def dns_lookup(domain="", attempts = 0):
	"""
		Here the domain name will be checked for all the records. If any records are present, then it will return the data else. It will return an empty list
	"""
	try:
		if domain == "":
			raise dns.resolver.NoAnswer
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

def dns_reverse_lookup(ip="0.0.0.0", attempts=0):
	"""
		This function is used to perform the reverse-dns lookups. We will not be using it much but could be a good addition. It is not yet complete
	"""
	try:
		if ip == "0.0.0.0":
			raise dns_resolver.NoAnswer
		else:
			answer = dns.reversename.from_address(ip)
			return answer
	
	except (dns_resolver.NXDOMAIN, dns_resolver.NoAnswer):
		print("Error")
		return []
	
	except (dns_resolver.Timeout):
		if attempts > 3:
			return []
		else:
			print("Error")
			return dns_reverse_lookup(ip, attempts + 1)
	except Exception as e:
		print("Error", e)
		return []

def isDomainAlive(domain_name):
	if domain_name == "":
		return False
	else:
		target_ip = dns_lookup(domain_name)[0]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		my_endpoint = ("127.0.0.1", 15000)
		socket.bind(my_endpoint)

domain = "music.youtube.com"

res = dns_lookup(domain)

print(res)
