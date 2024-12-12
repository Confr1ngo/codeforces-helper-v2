import storage
import config

import requests
import secrets
import hashlib
import time
import json
import os

get_salt      = lambda len: ''.join([secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(len)])
list_to_param = lambda lst: '&'.join([f'{i[0]}={i[1]}' for i in lst])
get_signature = lambda salt,operation,params: hashlib.sha512(f'{salt}/{operation}?{list_to_param(sorted(params))}#{storage.storage['secret']}'.encode()).hexdigest()

def request_json(operation:str,params:list):
	key=storage.storage['key']
	salt=get_salt(6)
	url=f'https://codeforces.com/api/{operation}?{list_to_param(params)}&lang=en&apiKey={key}&time={int(time.time())}'
	url=f'{url}&apiSig={salt}{get_signature(salt,operation,params+[['lang','en'],['apiKey',key],['time',int(time.time())]])}'
	return requests.get(url).json()

def access_api(operation:str,params:list):
	return request_json(operation,params)

def access_cache(operation:str,params:list,enforce_update:bool=False):
	if config.enable_cache and operation in ('problemset.problems','user.status'):
		if not enforce_update and os.path.exists(f'cache.{operation}.json'):
			with open(f'cache.{operation}.json','r') as f:
				data=json.load(f)
				if time.time()-data['lastupdate']<config.cache_expires:
					del data['lastupdate']
					return data['data']
		data=access_api(operation,params)
		with open(f'cache.{operation}.json','w') as f:
			json.dump({'lastupdate':time.time(),'data':data},f)
		return data
	return access_api(operation,params)
