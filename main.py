# -*- coding: utf-8 -*-

title=r'''
   ______________  __     __                        ___ 
  / ____/ ____/ / / /__  / /___  ___  _____   _   _|__ \
 / /   / /_  / /_/ / _ \/ / __ \/ _ \/ ___/  | | / /_/ /
/ /___/ __/ / __  /  __/ / /_/ /  __/ /      | |/ / __/ 
\____/_/   /_/ /_/\___/_/ .___/\___/_/       |___/____/ 
                       /_/                              
'''

'''
Codeforces Helper written by Confringo.
The core code is rewritten to make it more maintainable.
'''

import rich.traceback
import rich.console
import storage
import config
import sys

import unsolved
import randprob
import contest
import filters
import monitor
import problem
import friend
import rating
import stats
import check
import blog
import rank
import sync
import user

VERSION='2.0.0-pre1'
module_list={}
maxlen=0

def richprint(*args):
	storage.storage['console'].print(*args)

def init()->bool:
	try:
		f=open(config.filename,'r',encoding='utf-8')
		text=[i.replace('\r','').replace('\n','') for i in f.readlines()]
		f.close()
		if len(text)!=3:
			richprint(f'[bold red]ERR  File error. Check file {config.filename}.[/bold red]')
			return False
	except:
		richprint(f'[bold red]ERR  File error. Check file {config.filename}.[/bold red]')
		return False
	storage.storage['self_handle']=text[0]
	storage.storage['key']=text[1]
	storage.storage['secret']=text[2]
	richprint(f'[bold green]OK   Successfully read configuration file.[/bold green]')
	return True

def register_module(module):
	global maxlen
	module_list[module.name]=module
	maxlen=max(maxlen,len(module.name))

def register_modules():
	register_module(blog)
	register_module(check)
	register_module(contest)
	register_module(friend)
	register_module(filters)
	register_module(monitor)
	register_module(problem)
	register_module(randprob)
	register_module(rank)
	register_module(rating)
	register_module(stats)
	register_module(sync)
	register_module(unsolved)
	register_module(user)

def main():
	rich.traceback.install(show_locals=True)
	storage.storage['console']=rich.console.Console()
	if not init():
		exit(0)
	args=sys.argv[1:]
	register_modules()
	if len(args)==0 or args[0]=='help':
		print(title)
		print('Version:',VERSION)
		print(f'Usage: {sys.argv[0]} <command> [args...]\n')
		print('Available commands:')
		for i in module_list:
			print(f'{i.ljust(maxlen)} - {module_list[i].description}')
	elif args[0] in module_list:
		module_list[args[0]].main(args[1:])
	else:
		richprint(f'[bold red]ERR  Unknown command {args[0]}.[/bold red]')

if __name__=='__main__':
	main()
