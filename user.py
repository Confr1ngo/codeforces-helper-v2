# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

description='Collect public information by handle.'
usage='user <handle1> handle2 ...'
name='user'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)<1:
		print('Usage:',usage)
		return
	get_user_info(*args)

def get_user_info(users:list[str])->None:
	handles=users[0]
	for i in range(1,len(users)): handles=handles+';'+users[i]
	response=access.access_cache('user.info',[['handles',handles]])
	table=[['Handle','Email','VK ID','Open ID','First Name','Last Name','Country','City','Organization','Contrib','Rank','Max Rank','Last Visit','Registration Time']]
	if response['status']=='OK':
		for i in response['result']:
			info=['email','vkId','openId','firstName','lastName','country','city','organization']
			row=[i['handle'],'','','','','','','','','','','','','']
			for j in range(1,9):
				if info[j-1] in i:
					row[j]=i[info[j-1]]
			i['contribution']=str(i['contribution'])
			if i['contribution']=='0':      row[9]='[bold grey0]0[/bold grey0]'
			elif i['contribution'][0]=='-': row[9]=f'[bold red]{i['contribution']}[/bold red]'
			else:                           row[9]=f'[bold green]+{i['contribution']}[/bold green]'
			if 'rank' in i:
				row[10]=f'{util.get_rank_string(i['rating'])} {util.get_rating_string(i['rating'])}'
				row[11]=f'{util.get_rank_string(i['maxRating'])} {util.get_rating_string(i['maxRating'])}'
			else:
				row[10]=row[11]='Unrated'
			if 'lastOnlineTimeSeconds' in i:   row[12]=str(util.format_time(i['lastOnlineTimeSeconds']))
			if 'registrationTimeSeconds' in i: row[13]=str(util.format_time(i['registrationTimeSeconds']))
			table.append(row)
		printer.print_table(table,['left','left','left','left','left','left','left','left','left','left','left','left','left','left'])
	else:
		print(f'[{util.time_now()}] [get_user_info] Failed. Error message:',response['comment'])
