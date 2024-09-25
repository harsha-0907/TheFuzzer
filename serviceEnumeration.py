#!/bin/python3

from packages import *


def nmapEnumeration(domain="", directory_path="", data_queue=[], attempts=1):
	"""This is a function that will be run parallely. So here data will be stored in the queues that support multi-processing"""
	if domain == "" or domain == " ":
		print("Empty")
		return ""
	# We will formulate the comand and execute it
	try:
		res = subprocess.run(["nmap", "-sV", domain, "-oN", f"{directory_path}nmap_{domain}.txt"], capture_output=True)
		# If the stderr is None, then flush the stdout
		if not res.stderr:	
			#return res.stdout.decode()
			data_queue.put((domain, res.stdout.decode()))
			return True 
		
		return False	
	
		# In case of any error attempt another t
	except subprocess.CalledProcessError:
		if attempts > 3:
			return False
		return performNmapVersionEnumeration(domain, directory_path, attempts+1)
	
	except Exception as e:
		return False


def serviceVersionEnumeration(domains=[]):
	"""This function will be used to enumerate all the  """
	max_processes = 2	# Let the maximum number processes be 5
	no_processes = 0; domain_cnt = 0; no_domains = len(domains)
	process_queue = set()	# To maintain the list of all active processes
	data_queue = multiprocessing.Queue()
	directory_path = ""; completed_domains = 0
	while completed_domains < no_domains:
		if len(process_queue) < max_processes and domain_cnt < len(domains):
			p = multiprocessing.Process(target=nmapEnumeration, args=(domains[domain_cnt], "", data_queue, ))
			process_queue.add(p); domain_cnt += 1
			p.start()
		
		set2 = set()
		for process in process_queue:
			if not process.is_alive():	# If the function has completed its execution
				process.join()
				completed_domains += 1
				set2.add(process)
		if set2 != set():
			process_queue = process_queue - set2
	
	nmapData = dict()
	while not data_queue.empty():
		domain, data = data_queue.get()
		nmapData[domain] = data
	
	return nmapData
		