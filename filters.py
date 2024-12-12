# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

import ast
import re

description='Filter submissions by given filters.'
usage='filter <handle> filter1 ...'
name='filter'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)<1 or len(*args)%2==0:
		print('Usage:',usage)
		return
	handle=args[0][0]
	filters={}
	raw_filters=args[0][1:]
	for i in range(0,len(raw_filters),2):
		if raw_filters[i] in ('recent','last','ratingeq','ratingle','ratingge','testsle','testsge','testseq','tag'):
			filters[raw_filters[i]]=ast.literal_eval(raw_filters[i+1])
		else:
			filters[raw_filters[i]]=raw_filters[i+1]
	filter_status(handle,filters)

def filter_status_list(handle:str,filters:dict)->list[list]:
	response=access.access_cache('user.status',[['handle',handle],['from','1'],['count','1000000000']],True)
	if response['status']=='OK':
		result=response['result']
		recent,last=len(result),0
		if 'recent' in filters: recent=max(1,filters['recent'])
		if 'last' in filters:   last=max(1,len(result)-filters['last'])
		if last>recent:         return []
		table=[]
		for i in result[last:recent]:
			try:    probid=str(i['problem']['contestId'])+i['problem']['index']
			except: probid=i['problem']['problemsetName']+i['problem']['index']
			try:    rating='*'+str(i['problem']['rating'])
			except: rating='Unrated'
			try:    i['verdict']=i['verdict']
			except: i['verdict']='IN_QUEUE'
			if 'testsge'       in filters and i['passedTestCount']<filters['testsge']:  continue
			if 'testsle'       in filters and i['passedTestCount']>filters['testsle']:  continue
			if 'testseq'       in filters and i['passedTestCount']!=filters['testseq']: continue
			if 'subid'         in filters and re.search(filters['subid'],str(i['id']))   is None: continue
			if 'rating'        in filters and re.search(filters['rating'],rating)        is None: continue
			if 'verdict'       in filters and re.search(filters['verdict'],i['verdict']) is None: continue
			if 'problemid'     in filters and re.search(filters['problemid'],probid)     is None: continue
			if 'ratingle'      in filters and (rating=='Unrated' or i['problem']['rating']>filters['ratingle']):  continue
			if 'ratingge'      in filters and (rating=='Unrated' or i['problem']['rating']<filters['ratingge']):  continue
			if 'ratingeq'      in filters and (rating=='Unrated' or i['problem']['rating']!=filters['ratingeq']): continue
			if 'timestamp'     in filters and re.search(filters['timestamp'],str(i['creationTimeSeconds'])) is None: continue
			if 'formattedtime' in filters and re.search(filters['formattedtime'],str(util.format_time(i['creationTimeSeconds']))) is None: continue
			if 'tag' in filters:
				if len(i['problem']['tags'])==0:
					continue
				conditions=filters['tag']
				tags=i['problem']['tags']
				if not util.check_if_tags_match(conditions,tags):
					continue
			temp=[
				str(util.format_time(i['creationTimeSeconds'])),
				str(i['id']),
				rating,
				probid,
				util.get_verdict_string(i['verdict']),
				str(i['timeConsumedMillis'])+' ms',
				str(i['memoryConsumedBytes']//1024)+' KB',
				str(i['passedTestCount']),
				i['programmingLanguage']
			]
			table.append(temp)
		return table
	print(f'[{util.time_now()}] [filter_status] Failed. Error message:',response['comment'])
	return []

def get_accepted_list(handle:str)->list[str]:
	return [i[3] for i in filter_status_list(handle,{'verdict':'^OK$'})]

def filter_status(handle:str,filters:dict)->None:
	table=[['Time','Submission ID','Rating','Problem','Verdict','Time Usage','Memory Usage','Tests Passed','Language']]+filter_status_list(handle,filters)
	printer.print_table(table,['center','center','center','center','center','right','right','right','left'])