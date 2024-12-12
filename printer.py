# -*- coding: utf-8 -*-

import rich.table
import storage

def print_table(lst:list[list],align:list)->None:
	console=storage.storage['console']
	table=rich.table.Table(show_header=True,header_style='bold magenta')
	for i in range(len(lst[0])):
		table.add_column(lst[0][i],justify=align[i])
	for i in range(1,len(lst)):
		table.add_row(*[*lst[i]])
	console.print(table)
