# -*- coding: utf-8 -*-

import filters
import util

description='Fetch and print all accepted submissions of a given handle.'
usage='check <handle>'
name='check'

def main(*args):
	if len(*args)!=1:
		print('Usage:',usage)
		return
	check(*args[0])

def check(handle:str)->None:
	filters.filter_status(handle,{'verdict':'^OK$','formattedtime':str(util.time_now())[:10]})
