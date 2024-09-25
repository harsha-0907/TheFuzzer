#!/bin/bash

# This program will be used tas the flow-control of the program
# This program will be running various programs.


from packages import *
from initProgram import *
from dnsresolution import *
from subDomainEnum import *
from serviceEnumeration import *

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
		

if __name__ == "__main__":
	try:		
		domain_name = sys.argv[1]
		a = Application(domain_name)
		#print(a.info, a.resume)
		if not a.resume:
			print("Domain Not Found")
			exit()
		# Starting the sub-domain enum
		print("Domain Found")
		print("Starting Sub-Domain Enum")
		subdomains = fetchSubDomains(domain_name) + [domain_name]
		print("Sub-Domain Enumeration Complete")
		a.info['sub-domains'] = subdomains
		a.dumpData()
		# Service Enumeration using nmap
		print("Starting Service-Version Enumeration")
		a.info['service-enum'] = serviceVersionEnumeration(subdomains)
		#print(res, type(res))
		a.dumpData()
		
	except IndexError:
		if len(sys.argv) < 2:
			print("Domain Name is Empty!!!")
		else:
			print("Error")
	except Exception as e:
		print("An Error has occured", e)
