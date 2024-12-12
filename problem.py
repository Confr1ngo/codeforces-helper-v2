# -*- coding: utf-8 -*-

import storage
import access
import util

description='Fetch information of given problem IDs.'
usage='problem <problem1> problem2 ...'
name='problem'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)!=1:
		print('Usage:',usage)
		return
	chk_problem(*args)

def chk_problem(problems:list[str])->None:
	response=access.access_cache('problemset.problems',[[]])
	if response['status']=='OK':
		result=[]
		for pp in problems:
			flag=False
			for i in response['result']['problems']:
				try:    probid=str(i['contestId'])+i['index']
				except: probid=i['problemsetName']+i['index']
				if pp==probid: result.append(i); flag=True; break
			if not flag: result.append({'ID':pp,'notfound':True})
		for i in result:
			if 'notfound' in i:
				print(i['ID']+':')
				print('Not found.\n')
			else:
				try:    probid=str(i['contestId'])+i['index']
				except: probid=i['problemsetName']+i['index']
				try:    rating=util.get_diff_string(i['rating'])
				except: rating='[bold grey0]Unrated[/bold grey0]'
				print(probid+':')
				print('Name          :',i['name'])
				richprint('Rating        :',rating)
				print('Tags          :',end=' ')
				print('; '.join(i['tags']))
				if len(i['tags'])==0: print('none')
	else:
		print(f'[{util.time_now()}] [chk_problem] Failed. Error message:',response['comment'])
