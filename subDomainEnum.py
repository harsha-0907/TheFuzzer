#!/bin/python3

from packages import *
from exceptions import *


def fetchRawSubDomains(domain_name=""):
	"""
		Here we will be fetching all the sub-domains of the given domain. 
		The next step will innvolve cleaning and checking the availability of the sub-domain
	"""
	try:
		if domain_name == "":
			raise InvalidDomainName("Domain Name is Empty")
		else:
			# Fetch sub-domains
			pass
			
	except InvalidDomainName as e:
		print("Error Code - ", e.error_code, " ", e)
		return []
	
res  = fetchRawSubDomains("")

print(res)
