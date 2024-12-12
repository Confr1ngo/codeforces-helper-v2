# -*- coding: utf-8 -*-

import filters
import storage
import printer
import util

import matplotlib.pyplot

description='Rank users by problems solved today or sum of rating.'
usage='rank <method> <handle>'
name='rank'

def richprint(*args):
	storage.storage['console'].print(*args)

def main(*args):
	if len(*args)<2:
		print('Usage:',usage)
		return
	get_rank(args[0])

def get_rank(args:list[str])->None:
	users=args[1:]
	amount=[]
	method=args[0]
	for i in users:
		print(f'[{util.time_now()}] Getting user '+i+'\'s status ...')
		stat=filters.filter_status_list(i,{'verdict':'^OK$','formattedtime':str(util.time_now())[:10]})
		accepted,temp=[[j[2],j[3]] for j in stat],[]
		for j in accepted:
			if j not in temp:
				temp.append(j)
		amount.append([len(temp),sum([int(j[0][1:]) for j in accepted if j[0]!='Unrated'])])
	sortLst=[]
	for i in range(len(users)):
		temp=[]
		if method=='ratinggraph': temp.append(amount[i][1])
		else:                     temp.append(amount[i][0])
		temp.append(users[i])
		sortLst.append(temp)
	sortLst=sorted(sortLst,reverse=True)
	if method in ('graph','ratinggraph'):
		x,y=[i[1] for i in sortLst],[i[0] for i in sortLst]
		matplotlib.pyplot.barh(x,y)
		matplotlib.pyplot.title('Today\'s Rankings')
		matplotlib.pyplot.ylabel('Handle')
		matplotlib.pyplot.xlabel(f'Amount of {'Problems' if method=='graph' else 'Rating'}')
		matplotlib.pyplot.show()
	else:
		table=[['Handle','Amount of Problems']]
		for i in range(len(sortLst)):
			table.append([sortLst[i][1],str(sortLst[i][0])])
		printer.print_table(table,['center','center'])
