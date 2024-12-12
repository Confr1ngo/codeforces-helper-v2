# -*- coding: utf-8 -*-

import filters
import storage
import printer
import problem

description='Fetch the unsolved problems of a given handle.'
usage='unsolved <handle> <format>'
name='unsolved'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)!=2:
		print('Usage:',usage)
		return
	chk_unsolved(*args[0])

def chk_unsolved(handle:str,print_method:str)->None:
	stat=filters.filter_status_list(handle,{})
	ac,unac,handled=[],[],[]
	result=[['Last Submission Time','Last Submission ID','Problem ID','Rating','Status','Test Passed']]
	for i in stat:
		if i[4].find('Accepted')!=-1: ac.append(i[3])
		else: unac.append([i[0],i[1],i[3],i[2],i[4],i[7]])
	ac=list(set(ac))
	for i in unac:
		if i[2] not in ac:
			if i[2] not in handled:
				if i[4].find('Partial')==-1:
					handled.append(i[2])
					result.append(i)
	if print_method=='filter':
		print(len(result)-1,'results found.')
		printer.print_table(result,['center','right','right','center','center','right'])
	else:
		result=result[1:]
		problems=[]
		for i in result:
			problems.append(i[2])
		problem.chk_problem(problems)
