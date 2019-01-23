"""
This script needs the following files:

free_email_domains.py			for list of public email domains
exclude_email_hostnames.py		a dict of general email hostnames

"""

import re
from .free_email_domains import free_email_domain_list
from .exclude_email_hostnames import exclude_hostname_dict
import bisect

free_ed_length = len(free_email_domain_list)
regex_email = re.compile(r'([A-Za-z][a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})')
regex_email_only = re.compile(r'^[A-Za-z][a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}$')
regex_segs = re.compile(r'[A-Za-z0-9]+')

def retrieve_email_from_string(email):
	"""
	Retrieve all email patterns from a string.
	"""
	res_iter = regex_email.finditer(email)
	return (res.group(0) for res in res_iter)

def is_public_domain(email_domain):
	pos = bisect.bisect_left(free_email_domain_list, email_domain.strip().lower())
	if pos >= free_ed_length or free_email_domain_list[pos] != email_domain:
		return False
	else:
		return True

def is_good_hostname(hostname):
	hostname = hostname.strip().lower()
	if hostname in exclude_hostname_dict and exclude_hostname_dict[hostname] == 1:
		return (False, " hostname excluded")
	if "www." in hostname:
		return (False, "hostname contains www")
	if len(hostname) > 30:
		return (False, "hostname too long")
	res = regex_segs.findall(hostname)
	if len(res) > 4:
		return (False, "hostname too many segs")
	for seg in res:
		if len(seg) > 19:
			return (False, "hostname seg too long")
	return (True, "NA")

def is_good_domain(domain):
	domain = domain.strip().lower()
	if domain == "":
		return (False, "domain empty")
	if is_public_domain(domain):
		return (False, "domain public")
	if "www." in domain:
		return (False, "domain contains www")
	res = regex_segs.findall(domain)
	if len(res) > 5:
		return (False, "domain too many segs")
	for seg in res:
		if len(seg) > 30:
			return (False, "domain seg too long")
	return (True, "NA")

def is_good_email(email):
	email = email.strip().lower()
	if regex_email_only.search(email) is None:
		return (False, "email bad pattern")
	hostname, domain = email.split('@')
	flag, reason = is_good_hostname(hostname)
	if not flag:
		return (flag, reason)
	else:
		return is_good_domain(domain)



# if __name__ == "__main__":


	# print(is_good_email("bcaab55ecefere@wps.com"))
	# res = retrieve_email_from_string("wk.chan/pauline.law@towngas.com")
	# print('First test...')
	# print(res)
	# print('*' * 10, '\n')


	# res = retrieve_email_from_string("wk.chan/pauline.law@towngas/com")
	# print('Second test...')
	# print(res)
	# print('*' * 10, '\n')

	# res = retrieve_email_from_string("sl@easthope.sg/liu.xiangyu@easthope.cn")
	# print('Third test...')
	# print(res)
	# print('*' * 10, '\n')

	# print(is_public_domain('gmail.com'))