#!/usr/bin/env python

import argparse
import os, sys, re
import sqlite3
from commit_parser import commit
from patterns import err_patterns
from logparser import LogPatchSplitter

# arguments need in analyze
parser = argparse.ArgumentParser()
parser.add_argument('-err_report', help='error report of compiling', required=True)
parser.add_argument('-diff_db', help='difference database of kernel_api_decl', required=True)
parser.add_argument('-old_ver', help='old linux version, like v3.4', required=True)
parser.add_argument('-new_ver', help='new linux version, like v3.4', required=True)
parser.add_argument('-linux_git', help='the path to linux git tree directory', required=True)
args = parser.parse_args()

# check if arguments are valid
if not os.path.exists(args.err_report):
	print "[Error] \'" + args.err_report + "\' is not existed."
	quit()
if not os.path.exists(args.diff_db):
	print "[Error] \'" + args.diff_db + "\' is not existed."
	quit()
if not os.path.exists(args.linux_git):
	print "[Error] \'" + args.linux_git + "\' is not existed."
	quit()

# some useful variables
CUR_DIR = os.path.abspath(os.curdir)
ERR_REPORT = os.path.abspath(args.err_report)
DIFF_DB = os.path.abspath(args.diff_db)
LINUX_GIT = os.path.abspath(args.linux_git)
OLD_VER = args.old_ver
NEW_VER = args.new_ver

# connect to diff database
conn_diff = sqlite3.connect(args.diff_db)
CURSOR_DIFF = conn_diff.cursor()

# check if the linux version numbers is valid
os.chdir(LINUX_GIT)
tags = os.popen('git tag').read().strip().split('\n')
if len(tags) <= 1:
	print "[Error] linux git tree is invalid."
	quit()
if not args.old_ver in tags:
	print "[Error] linux version " + args.old_ver + " is not in linux git tree."
	quit()
if not args.new_ver in tags:
	print "[Error] linux version " + args.new_ver + " is not in linux git tree."
	quit()

# class of diff result
class Diff:
	def __init__(self, name, fname, start_line, old_decl, old_file, new_decl, new_file, type_chg):
		self.name = name
		self.fname = fname
		self.start_line = start_line
		self.old_decl = old_decl
		self.old_file = old_file
		self.new_file = new_file
		self.new_decl = new_decl
		self.type_chg = type_chg

	def __str__(self):
		ret = ''
		ret += "DECL NAME:\t" + self.name + '\n'
		ret += "FILE NAME:\t" + self.fname + '\n'
		ret += "CHANGE TYPE:\t" + self.type_chg + '\n'
		if self.type_chg == "ADD":
			ret += "DECLARATION:\t" + self.new_decl + '\n'
		if self.type_chg == "DELETE":
			ret += "DECLARATION:\t" + self.old_decl + '\n'
		if self.type_chg == "FILE CHANGED" or self.type_chg == "ALL CHANGED":
			ret += "ORIGIN FILE:\t" + self.old_file + '\n'
			ret += "CURRENT FILE:\t" + self.new_file + '\n'
		if self.type_chg == "DECL CHANGED" or self.type_chg == "ALL CHANGED":
			ret += "ORIGIN DECL:\t" + self.old_decl + '\n'
			ret += "CURRENT DECL:\t" + self.new_decl + '\n'
		return ret

# the class of error
class Error:
	"""
		Error is class of error which is extracted from error report,
		and it stores the detailed information of each error, the reason
		will be contained too
	"""

	def __init__(self, info, code, kind, api):
		self.info = info
		self.code = code
		self.kind = kind
		self.reason = ''
		self.api = api
		self.diff_result = []
		self.commit = []
		# suggestion is some patch of linux with similar change
		self.suggestion = []
	
	def get_err_info(self):
		ret = self.info + self.code
		return ret

	def interpret(self):
		if self.api == '' or len(self.diff_result) == 0:
			print "[ERROR]: information is incomplete, can not interpret."
			return
		self.commit = commit_locate(self.api, self.diff_result[0].fname, self.kind)
		print "[INTERPRET] this error may be caused by the commit following\n"
		for c in self.commit:
			print c.filter_output(self.api)
		self.suggestion = suggestion_search(self.api, self.diff_result[0].type_chg)
		print "[INTERPRET] and maybe you could fix this error as the following commit does\n"
		for s in self.suggestion:
			print s.filter_output(self.api)

# extract api which has problem from expected error information into problems
def expected_handle(info, next_line, api_name):
	global problems
	code = next_line.strip().split(' ')
	count = len(code) - 1
	while count >= 0:
		if code[count].find(api_name) >= 0:
			break
		count -= 1
	api = code[count - 1]
	error = Error(info, next_line, 'expected', api)
	problems['expected'].append(error)

def general_handle(info, next_line, api_name, type_name):
	global problems
	error = Error(info, next_line, type_name, api_name)
	problems[type_name].append(error)

# get the relative path of LINUX_GIT from abspath
def get_relative_path(abspath):
	os.chdir(LINUX_GIT)
	fname = os.path.basename(abspath)
	cmd = 'find -name "' + fname + '"'
	flist = os.popen(cmd).read().strip().split('\n')
	if flist[0] == '':
		os.popen('git checkout ' + OLD_VER)
		flist = os.popen(cmd).read().strip().split('\n')
	os.chdir(CUR_DIR)
	if flist[0] == '':
		print "[WARNING]: " + fname + " is not existed."
		return fname
	for f in flist:
		if abspath.find(f[1:]) >= 0:
			return f
	print "[WARNING]: can not find relative path of '" + fname + "'."
	return fname

# locate commits which change the api
def commit_locate(api, fname, kind):
	rpath = get_relative_path(fname)
	os.chdir(LINUX_GIT)
	git_cmd = ''
	if kind == 'arguments':
		git_cmd = "git log --no-merges -p -G'"
	else:
		git_cmd = "git log --no-merges -p -S'"
	git_cmd += api + "' " + OLD_VER + ".." + NEW_VER + " -- " + rpath[2:]
	# split all commits found
	found = os.popen(git_cmd)
	patches = LogPatchSplitter(found)
	commits = []
	# construct commit object for each commit with patch
	for p in patches:
		tmpc = commit()
		if tmpc.full_commit_parser(p) == True:
			commits.append(tmpc)
	os.chdir(CUR_DIR)
	return commits

def suggestion_search(api, chg_type):
	os.chdir(LINUX_GIT)
	git_cmd = ''
	if chg_type == 'DECL CHANGED':
		git_cmd = "git log --no-merges -p -G'"
	else:
		git_cmd = "git log --no-merges -p -S'"
	git_cmd += api + "' " + OLD_VER + ".." + NEW_VER + " -- drivers/" 
	patches = LogPatchSplitter(os.popen(git_cmd))
	commits = []
	for p in patches:
		tmpc = commit()
		if tmpc.full_commit_parser(p) == True:
			commits.append(tmpc)
	os.chdir(CUR_DIR)
	return commits

# search diff results from database
def search_diff_results(problems):
#	errs = problems['expected']
	for ty in problems:
		errs = problems[ty]
		for err in errs:
			sql_cmd = "select * from decls_chg where name=\'" + err.api + "\'"
			CURSOR_DIFF.execute(sql_cmd)
			result = CURSOR_DIFF.fetchall()
			if len(result) > 0:
				for r in result:
					diff = Diff(r[0],r[1],r[2],r[4],r[5],r[6],r[7],r[8])
					err.diff_result.append(diff)
			sql_cmd = "select * from macros_chg where name=\'" + err.api + "\'"
			CURSOR_DIFF.execute(sql_cmd)
			result = CURSOR_DIFF.fetchall()
			if len(result) > 0:
				for r in result:
					diff = Diff(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7])
					err.diff_result.append(diff)

# analyze error report, extract error type and reason
err_file = open(ERR_REPORT, 'r')
# store error type and the corresponding apis, the key is error type
problems = {}
problems['expected'] = []
problems['implicit'] = []
problems['undeclared'] = []
problems['arguments'] = []

for line in err_file:
	m = err_patterns['expected'].match(line)
	if m:
		expected_handle(line, err_file.next(), m.group(3))
		continue
	m = err_patterns['implicit'].match(line)
	if m:
		general_handle(line, err_file.next(), m.group(3), 'implicit')
		continue
	m = err_patterns['undeclared'].match(line)
	if m:
		general_handle(line, err_file.next(), m.group(3), 'undeclared')
	m = err_patterns['arguments'].match(line)
	if m:
		general_handle(line, err_file.next(), m.group(3), 'arguments')
		continue

print len(problems['arguments'])
search_diff_results(problems)

for e in problems['undeclared']:
	print "----Error information as follows:"
	print "\t" + e.get_err_info()
	print "----Related differency analysis results as follows:"
	print e.diff_result[0]
	e.interpret()

#problems['undeclared'][6].interpret()



