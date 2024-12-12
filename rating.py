# -*- coding: utf-8 -*-

import storage
import printer
import access
import util

description='Fetch rating changes of a given handle.'
usage='rating <handle>'
name='rating'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)!=1:
		print('Usage:',usage)
		return
	get_rating_changes(*args[0])

def get_rating_changes(handle:str)->None:
	response=access.access_cache('user.rating',[['handle',handle]])
	table=[['#','Contest ID','Contest Name','Rank','Update Time','Old Rating','New Rating','Change']]
	if response['status']=='OK':
		for k in range(len(response['result'])):
			i=response['result'][k]
			temp=[
				str(k+1),str(i['contestId']),i['contestName'],str(i['rank']),
				str(util.format_time(i['ratingUpdateTimeSeconds'])),
				f'{util.get_rank_abbr(i['oldRating'])} {util.get_rating_string(i['oldRating'])}',
				f'{util.get_rank_abbr(i['newRating'])} {util.get_rating_string(i['newRating'])}'
			]
			if i['oldRating']==i['newRating']: temp.append('[bold grey0]0[/bold grey0]')
			elif i['oldRating']<i['newRating']: temp.append(f'[bold green]+{i['newRating']-i['oldRating']}[/bold green]')
			else: temp.append(f'[bold red]{i['newRating']-i['oldRating']}[/bold red]')
			table.append(temp)
		printer.print_table(table,['left','center','left','right','center','right','right','right'])
	else:
		print(f'[{util.time_now()}] [get_rating_changes] Failed. Error message:',response['comment'])
