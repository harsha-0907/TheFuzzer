#!/bin/python3

from packages import *
from exceptions import *
from initProgram import *


def fetchRawSubDomains(domain_name="", enable_bruteforce=False, engines=None):
	"""
		Here we will be fetching all the sub-domains of the given domain. 
		The next step will innvolve cleaning and checking the availability of the sub-domain
	"""
	try:
		if domain_name == "":
			raise InvalidDomainName("Domain Name is Empty")
		else:
			# Fetch sub-domains to the file "raw_domains.txt"
			no_threads = 20	# For testing
			subdomains = sub.main(domain_name, no_threads, savefile=False, ports=None, silent=True, verbose=False, enable_bruteforce=enable_bruteforce, engines=engines)
			return subdomains
	except InvalidDomainName as e:
		print("Error Code - ", e.error_code, " ", e)
		return []

def filterDomains(total_subdomains = [], filepath="filter.txt"):
	"""
		Remove the out-of-scope sub-domains from the raw sub-domains.
	"""
	
	# First fetch all the restricted domains from the file path
	restricted_subdomains = set(readFileToList(file_path))
	inscope_subdomains = set(total_subdomains) - restricted_subdomains
	return list(inscope_subdomains)
	
	
def filterActiveSubDomains(total_subdomains):
	if total_subdomains == []:
		return []
	
	
res  = fetchRawSubDomains("mvgrce.com")

print(res)
