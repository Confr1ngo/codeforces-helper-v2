# -*- coding: utf-8 -*-

import storage
import access
import util

description='Synchronize local cache.'
usage='sync'
name='sync'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	synch()

def synch():
	print(f'[{util.time_now()}] Synchronizing problemset ...')
	access.access_cache('problemset.problems',[],True)
	print(f'[{util.time_now()}] Synchronizing user status ...')
	access.access_cache('user.status',[['handle',storage.storage['self_handle']],['from','1'],['count','1000000000']],True)
