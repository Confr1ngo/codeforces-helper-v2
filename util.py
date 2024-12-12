# -*- coding: utf-8 -*-

import datetime
import copy
import time
import re

format_time = lambda t: datetime.datetime.fromtimestamp(t)
time_now    = lambda  : format_time(int(time.time()))

def check_if_tags_match(conditions:list,tags:list)->bool:
	conditions_temp=copy.deepcopy(conditions)
	method=conditions[-1]
	for i in range(len(conditions_temp)-1):
		if isinstance(conditions_temp[i],str):
			flag=False
			for j in tags:
				if re.search(conditions_temp[i],j) is not None:
					flag=True
					break
			conditions_temp[i]=flag
		else:
			conditions_temp[i]=check_if_tags_match(conditions_temp[i],tags)
		if method=='and' and not conditions_temp[i]: return False
		if method=='or'  and     conditions_temp[i]: return True
		if method=='not' and     conditions_temp[i]: return False
	return method!='or'

# I'm sure this IS NOT the best way to do this, but it works.
# So I'm not going to change it.

def get_rank_string(rating:int)->str:
	if rating==0:   return 'Unrated'
	if rating<1200: return '[bold grey62]Newbie[/bold grey62]'
	if rating<1400: return '[bold dark_green])Pupil[/bold dark_green]'
	if rating<1600: return '[bold cyan]Specialist[/bold cyan]'
	if rating<1900: return '[bold deep_sky_blue4]Expert[/bold deep_sky_blue4]'
	if rating<2100: return '[bold purple]Candidate Master[/bold purple]'
	if rating<2300: return '[bold orange1]Master[/bold orange1]'
	if rating<2400: return '[bold orange1]International Master[/bold orange1]'
	if rating<2600: return '[bold red]Grandmaster[/bold red]'
	if rating<3000: return '[bold red]International Grandmaster[/bold red]'
	if rating<4000: return '[bold black]L[/bold black][bold red]egendary Grandmaster[/bold red]'
	return '[bold black]Tourist[/bold black]'

def get_rating_string(rating:int)->str:
	if rating==0:   return ''
	if rating<1200: return f'[bold grey62]{rating}[/bold grey62]'
	if rating<1400: return f'[bold dark_green]{rating}[/bold dark_green]'
	if rating<1600: return f'[bold cyan]{rating}[/bold cyan]'
	if rating<1900: return f'[bold deep_sky_blue4]{rating}[/bold deep_sky_blue4]'
	if rating<2100: return f'[bold purple]{rating}[/bold purple]'
	if rating<2400: return f'[bold orange1]{rating}[/bold orange1]'
	if rating<4000: return f'[bold red]{rating}[/bold red]'
	return f'[bold black]{rating}[/bold black]'

def get_verdict_string(verdict:str)->str:
	if verdict=='OK':                        return '[bold green]Accepted[/bold green]'
	if verdict=='FAILED':                    return '[bold orange1]Judgement Failed[/bold orange1]'
	if verdict=='SKIPPED':                   return '[bold grey0]Skipped[/bold grey0]'
	if verdict=='PARTIAL':                   return '[bold orange1]Partially Correct[/bold orange1]'
	if verdict=='TESTING':                   return '[bold cyan]Judging[/bold cyan]'
	if verdict=='CRASHED':                   return '[bold grey0]Crashed[/bold grey0]'
	if verdict=='REJECTED':                  return '[bold grey0]Rejected[/bold grey0]'
	if verdict=='IN_QUEUE':                  return '[bold grey0 u]In queue[/bold grey0 u]'
	if verdict=='CHALLENGED':                return '[bold orange1]Hacked[/bold orange1]'
	if verdict=='WRONG_ANSWER':              return '[bold bright_red]Wrong Answer[/bold bright_red]'
	if verdict=='RUNTIME_ERROR':             return '[bold violet]Runtime Error[/bold violet]'
	if verdict=='SECURITY_VIOLATED':         return '[bold grey0]Security Violated[/bold grey0]'
	if verdict=='COMPILATION_ERROR':         return '[bold grey0 u]Compilation Error[/bold grey0 u]'
	if verdict=='PRESENTATION_ERROR':        return '[bold blue]Presentation Error[/bold blue]'
	if verdict=='TIME_LIMIT_EXCEEDED':       return '[bold blue]Time Limit Exceeded[/bold blue]'
	if verdict=='MEMORY_LIMIT_EXCEEDED':     return '[bold blue]Memory Limit Exceeded[/bold blue]'
	if verdict=='IDLENESS_LIMIT_EXCEEDED':   return '[bold blue]Idleness Limit Exceeded[/bold blue]'
	if verdict=='INPUT_PREPARATION_CRASHED': return '[bold grey0]Input Preparation Crashed[/bold grey0]'
	return f'[bold bright_red]{verdict}[/bold bright_red]'

def get_diff_string(diff:int)->str:
	if diff<=1200: return f'[bold green1]{diff}[/bold green1]'
	if diff<=1600: return f'[bold green]{diff}[/bold green]'
	if diff<=2000: return f'[bold green_yellow]{diff}[/bold green_yellow]'
	if diff<=2400: return f'[bold yellow1]{diff}[/bold yellow1]'
	if diff<=2800: return f'[bold orange1]{diff}[/bold orange1]'
	if diff<=3200: return f'[bold orange_red1]{diff}[/bold orange_red1]'
	return f'[bold bright_red]{diff}[/bold bright_red]'


def get_rank_abbr(rating:int)->str:
	if rating==0:   return 'Unrated'
	if rating<1200: return '[bold grey62]NB[/bold grey62]'
	if rating<1400: return '[bold dark_green]PPL[/bold dark_green]'
	if rating<1600: return '[bold cyan]SPL[/bold cyan]'
	if rating<1900: return '[bold deep_sky_blue4]EXP[/bold deep_sky_blue4]'
	if rating<2100: return '[bold purple]CM[/bold purple]'
	if rating<2300: return '[bold orange1]MST[/bold orange1]'
	if rating<2400: return '[bold orange1]IMST[/bold orange1]'
	if rating<2600: return '[bold red]GM[/bold red]'
	if rating<3000: return '[bold red]IGM[/bold red]'
	if rating<4000: return '[bold black]L[/bold black][bold red]GM[/bold red]'
	return '[bold black]TRS[/bold black]'
