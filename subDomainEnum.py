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
			#print(subdomains)
			return subdomains
	except InvalidDomainName as e:
		print("Error Code - ", e.error_code, " ", e)
		return []

def filterDomains(total_subdomains = [], filepath="restricted_domains.txt"):
	"""
		Remove the out-of-scope sub-domains from the raw sub-domains.
	"""
	
	# First fetch all the restricted domains from the file path
	restricted_subdomains = set(readFileToList(filepath))
	#print(restricted_subdomains)
	inscope_subdomains = set(total_subdomains) - restricted_subdomains
	return list(inscope_subdomains)
	
	
def filterActiveDomains(total_subdomains):
	if total_subdomains == []:
		return []
	alive_domains = []
	for sub_domain in total_subdomains:
		if isAlive(sub_domain):
			alive_domains.append(sub_domain)
	
	return alive_domains

def isAlive(domain, attempts=0):
	""" We will be using httprobe to determine if a domain is active or in-active"""
	try:
		cmd1 = subprocess.Popen(["echo", domain], stdout=subprocess.PIPE)
		res = subprocess.Popen(["httprobe"], stdin=cmd1.stdout, stdout=subprocess.PIPE)
		cmd1.stdout.close()
		res = res.communicate()[0].decode()
		if res != "":
			# The domain is active
			#print(domain, "Is active")
			return True
		else:
			return False
	except subprocess.SubprocessError as e:
		if attempts > 3:
			return False
		return isAlive(domain, attempt+1)

def fetchSubDomains(domain_name, restricted_domains="restricted_domains.txt"):
	total_subdomains = fetchRawSubDomains(domain_name)
	#print("Fetched Raw DOmains", flush=True)
	total_subdomains[:] = filterDomains(total_subdomains, restricted_domains)
	total_subdomains[:] = filterActiveDomains(total_subdomains)
	return total_subdomains
	
