# -*- coding: utf-8 -*-

import storage
import access
import util

import tkinter
import time

description='Monitor accepted submissions of given handles.'
usage='monitor <handle1> handle2 ...'
name='monitor'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)<1:
		print('Usage:',usage)
		return
	monitor(args[0])

def show_window(subtime:str,handle:str,problem:dict)->None:
	try:    rating='*'+str(problem['rating'])
	except: rating='Unrated'
	try:    probid=str(problem['contestId'])+problem['index']
	except: probid=problem['problemsetName']+problem['index']
	probname=problem['name']
	tags=problem['tags']
	tagstr='None' if len(tags)==0 else '; '.join(tags)
	root=tkinter.Tk()
	root.attributes('-topmost',True)
	root.geometry('600x200+500+300')
	root.title('最新卷题提示')
	labelstr='Time:   '+subtime+'\nUser:   '+handle
	labelstr+='\nID:     '+probid+'\nTitle:  '+probname
	labelstr+='\nRating: '+rating+'\nTags:   '+tagstr
	labelstr+='\n\nPress Enter or Space to close this window.'
	label=tkinter.Label(root,text=labelstr,font=('Lucida Console',16),anchor='nw',justify='left')
	label.pack(anchor='nw')
	root.bind('<Return>',lambda x:root.destroy())
	root.bind('<space>',lambda x:root.destroy())
	root.mainloop()

def monitor(users):
	starttime=time.time()
	print(f'[{util.time_now()}] Start monitoring ... ')
	handled=[]
	while True:
		try:    response=access.access_cache('problemset.recentStatus',[['count','1000']])
		except: print(f'[{util.time_now()}] Request failed.'); time.sleep(2); continue
		if response['status']=='OK':
			print(f'[{util.time_now()}] Request was successful.')
			for i in response['result']:
				userfound=''
				flag=False
				for j in i['author']['members']:
					if j['handle'] in users:
						userfound=j['handle']
						flag=True
						break
				if not flag: handled.append(i['id']); continue
				if i['id'] in handled: continue
				if i['creationTimeSeconds']<starttime: handled.append(i['id']); continue
				try:
					verdict=i['verdict']
					if verdict not in ('OK','TESTING'):
						handled.append(i['id'])
						continue
					elif verdict!='OK':
						continue
				except: continue
				try:    probid=str(i['problem']['contestId'])+i['problem']['index']
				except: probid=i['problem']['problemsetName']+i['problem']['index']
				try:    rating='*'+str(i['problem']['rating'])
				except: rating='Unrated'
				print(f'[{util.format_time(i['creationTimeSeconds'])}] {userfound} accepted {probid} ({rating}).')
				show_window(str(util.format_time(i['creationTimeSeconds'])),userfound,i['problem'])
				handled.append(i['id'])
		else:
			print(f'[{util.time_now()}] [monitor] Failed. Error message:',response['comment'])
		time.sleep(5)

