# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

description='Print statistics information of a given handle.'
usage='stat <handle>'
name='stat'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)!=1:
		print('Usage:',usage)
		return
	get_stat(*args[0])

def get_stat(handle:str)->None:
	ratings,tags,verdicts,accepted={},{},{},[]
	response=access.access_cache('user.status',[['handle',handle],['from','1'],['count','1000000000']],True)
	if response['status']=='OK':
		result=response['result']
		print(f'{handle}\'s Statistics:\n')
		print('Recent 25 Submissions:')
		table=[['Time','Submission ID','Rating','Problem','Verdict','Time Usage','Memory Usage','Tests Passed','Language']]
		for i in result[:min(len(result),25)]:
			try:    probid=str(i['problem']['contestId'])+i['problem']['index']
			except: probid=i['problem']['problemsetName']+i['problem']['index']
			try:    rating='*'+str(i['problem']['rating'])
			except: rating='Unrated'
			temp=[
				str(util.format_time(i['creationTimeSeconds'])),
				str(i['id']),
				rating,
				probid,
				util.get_verdict_string(i['verdict'] if 'verdict' in i else 'IN_QUEUE'),
				str(i['timeConsumedMillis'])+' ms',
				str(i['memoryConsumedBytes']//1024)+' KB',
				str(i['passedTestCount']),
				i['programmingLanguage']
			]
			table.append(temp)
		printer.print_table(table,['center','center','center','center','center','right','right','right','left'])
		for i in result:
			verdict=i['verdict'] if 'verdict' in i else 'IN_QUEUE'
			try:    temp=verdicts[verdict]; verdicts[verdict]=temp+1
			except: verdicts[verdict]=1
			try:    probid=str(i['problem']['contestId'])+i['problem']['index']
			except: probid=i['problem']['problemsetName']+i['problem']['index']
			if verdict=='OK' and probid not in accepted:
				accepted.append(probid)
				rating=0
				try:    rating=i['problem']['rating']
				except: rating=-1
				try:    temp=ratings[rating]; ratings[rating]=temp+1
				except: ratings[rating]=1
				for j in i['problem']['tags']:
					try:    temp=tags[j]; tags[j]=temp+1
					except: tags[j]=1
		v_lst=sorted(verdicts.items(),key=lambda x:x[1],reverse=True)
		t_lst=sorted(tags.items(),key=lambda x:x[1],reverse=True)
		r_lst=sorted(ratings.items())
		print('\nVerdict Statistics:')
		total=0
		for i,j in v_lst: total+=j
		table=[['Verdict','Count','Percentage'],['Total',str(total),'100.000%']]
		for i,j in v_lst: table.append([util.get_verdict_string(i),str(j),str(int(round(j*100000/total))/1000)+'%'])
		printer.print_table(table,['center','right','right'])

		print('\nTag Statistics:')
		table=[['Tag','Count','Percentage'],['Total',str(len(accepted)),'100.000%']]
		for i,j in t_lst: table.append([i,str(j),str(int(round(j*100000/len(accepted)))/1000)+'%'])
		printer.print_table(table,['right','right','right'])

		print('\nDifficulty Statistics:')
		table=[['Rating','Accepted','Percentage'],['Total',str(len(accepted)),'100.000%']]
		for i,j in r_lst:
			if i==-1:
				table.append(['Unrated',str(j),str(int(round(j*100000/len(accepted)))/1000)+'%'])
			else:
				table.append(['*'+str(i),str(j),str(int(round(j*100000/len(accepted)))/1000)+'%'])
		printer.print_table(table,['right','right','right'])
	else:
		print(f'[{util.time_now()}] [get_stat] Failed. Error message:',response['comment'])
