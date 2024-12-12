# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

description='Fetch your friends\' status.'
usage='friend'
name='friend'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	get_friend()

def get_friend():
	print('Friend status:',)
	table=[['Handle','Status']]
	t1=access.access_cache('user.friends',[['onlyOnline','true']])
	t2=access.access_cache('user.friends',[['onlyOnline','false']])
	if t1['status']=='OK' and t2['status']=='OK':
		for i in t2['result']:
			if i in t1['result']: table.append([i,'[green]Online[/green]'])
			else:                 table.append([i,'[red]Offline[/red]'])
		printer.print_table(table,['center','center'])
	else:
		if t1['status']!='OK':
			print(f'[{util.time_now()}] [get_friend] Failed. Error message:',t1['comment'])
		if t2['status']!='OK':
			print(f'[{util.time_now()}] [get_friend] Failed. Error message:',t2['comment'])
