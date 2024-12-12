# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

description='Fetch blog entries of a specified user.'
usage='blog <handle>'
name='blog'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)!=1:
		print('Usage:',usage)
		return
	get_blog(*args[0])

def get_blog(handle:str):
	print(handle+'\'s Blogs:\n')
	t=access.access_cache('user.blogEntries',[['handle',handle]])
	if t['status']=='OK':
		table=[['Blog ID','Language','Publish Time','Update Time','Rating','Title']]
		for i in t['result']:
			i['rating']=str(i['rating'])
			if i['rating']=='0':      ratingstr='[bold grey0]0[/bold grey0]'
			elif i['rating'][0]=='-': ratingstr=f'[bold red]{i['rating']}[/bold red]'
			else:                     ratingstr=f'[bold green]+{i['rating']}[/bold green]'
			table.append([
				str(i['id']),i['locale'],str(util.format_time(i['creationTimeSeconds'])),
				str(util.format_time(i['modificationTimeSeconds'])),ratingstr,
				i['title'].replace('<p>','').replace('</p>','')
			])
		printer.print_table(table,['right','right','center','center','left','left'])
	else:
		print(f'[{util.time_now()}] [get_blog] Failed. Error message:',t['comment'])
