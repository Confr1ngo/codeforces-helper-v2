# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

import time

description='Fetch recent contests.'
usage='contest'
name='contest'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	get_contest()

def get_contest():
	response=access.access_cache('contest.list',[['gym','false']])
	if response['status']=='OK':
		table=[['#','Name','Status','Start Time','Duration','Before Start']]
		finishedsum=0
		for i in response['result']:
			temp=[str(i['id']),i['name'],'',str(util.format_time(i['startTimeSeconds'])),'','']
			if i['phase']=='FINISHED': temp[2]='[bold red]Finished[/bold red]'
			elif i['phase']=='CODING': temp[2]='[bold blue]Running[/bold blue]'
			else:                      temp[2]='[bold green]Before[/bold green]'
			totalsec=i['durationSeconds']
			day,hour,minute,second=str(totalsec//86400),str((totalsec%86400)//3600),str((totalsec%3600)//60),str(totalsec%60)
			hour,minute,second=hour.zfill(2),minute.zfill(2),second.zfill(2)
			temp[4]=f'{day}d {hour}:{minute}:{second}'
			totalsec=int(i['startTimeSeconds']-time.time())
			day,hour,minute,second=str(totalsec//86400),str((totalsec%86400)//3600),str((totalsec%3600)//60),str(totalsec%60)
			hour,minute,second=hour.zfill(2),minute.zfill(2),second.zfill(2)
			temp[5]=f'{day}d {hour}:{minute}:{second}'
			if i['phase']!='BEFORE':
				temp[5]='-'
				if finishedsum<5:
					if i['phase']=='FINISHED':
						finishedsum+=1
					table.append(temp)
				else:
					break
			else:
				table.append(temp)
		printer.print_table(table,['center','left','left','right','right','right'])
	else:
		print(f'[{util.time_now()}] [get_contest] Failed. Error message:',response['comment'])
