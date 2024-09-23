#!/bin/python3

# This module contains custom exceptions that might be encountered in the due course

class InvalidDomainName(Exception):
	""" Raised when the given domain is an invalid domain"""
	def __init__(self, message="Invalid Domain Name", code=401):
		super().__init__(message)
		self.error_code = code

