#!/usr/bin/env python

import re, sys, os
import rfc822, datetime
from logparser import LogPatchSplitter
from patterns import patterns

class commit:
	def __init__(self):
		self.commit_id = ''
		self.date = None
		self.author = ('', '')
		self.commit_log = ''
		# use 'filename' : 'diffcontent' to record patch
		self.patch = {}
		self.full_commit = None

	def full_commit_parser(self, fc):
		if len(fc) < 1:
			return False
	
		m = patterns['commit'].match(fc[0])
		if not m:
			return False
	
		cid = m.group(1)
		self.commit_id = cid
		self.full_commit = fc

		isPatch = False
		afterDate = False
		fname = ''
	
		for line in fc[1:]:
			m = patterns['merge'].match(line)
			if m:
				return False

			m = patterns['date'].match(line)
			if m:
				dt = rfc822.parsedate(m.group(2))
				self.date = datetime.date(dt[0], dt[1], dt[2])
				afterDate = True
				continue
			
			m = patterns['author'].match(line)
			if m:
				self.author = (m.group(1), m.group(2))
				continue

			m = patterns['diff'].match(line)
			if m:
				fname = m.group(2)[2:]
				self.patch[fname] = [line]
				isPatch = True
				continue

			if afterDate == True and isPatch == False:
				self.commit_log += line
				continue

			if isPatch == True:
				self.patch[fname].append(line)
				continue

		if fname == '' or isPatch == False or afterDate == False:
			return False
		return True

def main():
	patches = LogPatchSplitter(sys.stdin)

	commits = []
	for p in patches:
		tmpc = commit()
		if tmpc.full_commit_parser(p) == True:
			commits.append(tmpc)

#	for c in commits:
#		print "=========================================================================="
#		for l in c.patch:
#			print "------------------------------------------------------------------------"
#			for m in c.patch[l]:
#				print m,

	print len(commits)

if __name__ == '__main__':
	main()
