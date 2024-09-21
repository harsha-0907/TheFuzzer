#!/bin/python3

from packages import *

# Let the directory name be the url

def createDirectory(dirname="directory-1", path=""):
	"""
	Here the directory path will be relative to the program.
	If the directory exists then it will be removed
	New directory will be created and data updated
	"""
	if os.path.exists(path+dirname):
		print("Directory Exists")
		shutil.rmtree(path+dirname)
		print("Removed the tree")
	os.makedirs(path+dirname)
	if path == "":
		return os.getcwd() + '/' + dirname
	else:
		return path + '/' + dirname

dirname = sys.argv[1]
path = sys.argv[2]
print(dirname)

res = createDirectory(dirname, path)

print(res)
