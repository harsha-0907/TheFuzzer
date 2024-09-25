#!/bin/python3

from packages import *

def createDirectory(dirname="h", directory_path=""):
	"""
	Here the directory path will be relative to the program.
	If the directory exists then it will be removed
	New directory will be created and data updated
	"""
	if os.path.exists(directory_path+dirname):
		#print("Directory Exists")
		shutil.rmtree(directory_path+dirname)
		#print("Removed the tree")
	os.makedirs(directory_path+dirname)
	if directory_path == "":
		return os.getcwd() + '/' + dirname
	else:
		return directory_path + '/' + dirname

def dumpJSONData(json_data, file_path="variables.json"):
	"""
	Here we will load the json data to the variable.json file
	It will replace any existing file with the updated content
	For custom uses, provide the file_path with the complete path
	"""
	#print(file_path)
	with open(file_path, 'w') as file:
		#print("Data is being uploaded successfully")
		json.dump(json_data, file)
	#print("Data Loaded into the file successfully")
	return True

def readJSONData(file_path="variables.json"):
	"""
		Make sure that the file you are tyring to read is already present.
		This function will 
	"""
	__data = dict()
	try:
		if os.path.exists(file_path):
			with open(file_path, 'r') as file:
				__data = json.load(file)
	except json.JSONDecodeError:
		pass
	finally:		
		return __data

def updateJSONDataToFile(update_data, json_data=readJSONData()):
	"""
		In this function we will be updating the json data into the functions.
		Here we will only add a new key:value pair not updating any key:value pairs
	"""
	for i in update_data:
		json_data[i] = update_data[i]
	
	return json_data

def readFileToList(file_path="", seperator='\n'):
	if file_path == "":
		return []
	else:
		data = None
		if os.path.exists(file_path):
			with open(file_path, 'r') as file:
				data = file.read()
			lines = [i for i in data.split(seperator)]
			if lines != ['']:
				return lines
		return []




