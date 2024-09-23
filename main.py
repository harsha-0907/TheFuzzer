#!/bin/bash

# This program will be used tas the flow-control of the program
# This program will be running various programs.


from packages import *
from initProgram import *
from dnsresolution import *
from subDomainEnum.py import *

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
			print(dir_path)
			dumpJSONData(self.info, dir_path+'variables.json')
		# We have now populated the object with basic data for further work


if __name__ == "__main__":
	try:		
		domain_name = sys.argv[1]
		a = Application(domain_name)
		print(a.info, a.resume)
		if not a.resume:
			print("Process Stopped. Please check your input")
		
	except IndexError:
		if len(sys.argv) < 2:
			print("Domain Name is Empty!!!")
		else:
			print("Error")
	except Exception as e:
		print("An Error has occured")
	
