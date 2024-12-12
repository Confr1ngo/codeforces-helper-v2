# -*- coding: utf-8 -*-

import filters
import storage
import access
import util

import random
import time
import ast
import re

description='Get a random problem based on filter settings.'
usage='random <showtags> filter1 ...'
name='random'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)<1 or len(*args)%2==0:
		print('Usage:',usage)
		return
	showtag=args[0][0].lower()[0] in ('y','1','t')
	filters_={}
	raw_filters=args[0][1:]
	for i in range(0,len(raw_filters),2):
		if raw_filters[i] in ('ratingeq','ratingle','ratingge','tag'):
			filters_[raw_filters[i]]=ast.literal_eval(raw_filters[i+1])
		else:
			filters_[raw_filters[i]]=raw_filters[i+1]
	get_random_problem(filters_,showtag)

def get_random_problem(filters_:dict,showTags:bool)->None:
	handle=storage.storage['self_handle']
	print(f'[{util.time_now()}] Fetching user statistics ...')
	accepted=filters.get_accepted_list(handle)
	print(f'[{util.time_now()}] Fetching problemset ...')
	response=access.access_cache('problemset.problems',[])
	lst=[]
	if response['status']=='OK':
		for i in response['result']['problems']:
			try:    probid=str(i['contestId'])+i['index']
			except: probid=i['problemsetName']+i['index']
			if probid in accepted: continue
			try:    rating=str(i['rating'])
			except: rating='Unrated'
			if 'ratingle' in filters_ and (rating=='Unrated' or i['rating']> filters_['ratingle']): continue
			if 'ratingge' in filters_ and (rating=='Unrated' or i['rating']< filters_['ratingge']): continue
			if 'ratingeq' in filters_ and (rating=='Unrated' or i['rating']!=filters_['ratingeq']): continue
			if 'problemid' in filters_ and re.search(filters_['problemid'],probid) is None: continue
			if 'tag' in filters_:
				if len(i['tags'])==0: continue
				conditions=filters_['tag']
				tags=i['tags']
				if not util.check_if_tags_match(conditions,tags): continue
			lst.append(i)
		if len(lst)==0:
			print('No problem found')
			return
		random.seed(time.time())
		response=random.randint(0,len(lst)-1)
		try:    probid=str(lst[response]['contestId'])+lst[response]['index']
		except: probid=lst[response]['problemsetName']+lst[response]['index']
		print('Problem ID :',probid)
		print('Name       :',lst[response]['name'])
		if showTags:
			try:    richprint('Rating     :',util.get_diff_string(lst[response]['rating']))
			except: richprint('Rating     : [bold grey0]Unrated[/bold grey0]')
			print('Tags       :',end=' ')
			print('; '.join(lst[response]['tags']))
			if len(lst[response]['tags'])==0: print('none')
	else:
		print(f'[{util.time_now()}] [get_random_problem] Failed. Error message:',response['comment'])
