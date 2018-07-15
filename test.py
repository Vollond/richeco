import time
from pprint import pprint
import datetime
from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)
import json

p=10.0001
print(round(p,2))
print('_______')
print(time.ctime())
now=time.time()
print(now)
print(time.ctime(now))
now+=660
	
def new():
	jon = _default_data()
	jon["build"]["n"]=0
	jon["build"]["workers"]=0
	jon["build"]["warrior"]=0
	jon["build"]["exped"]=0
	jon["build"]["crystal"]=0
	jon["build"]["exp"]=0
	#jon=json.dumps(jon)
	return jon
	
jon=new()
print (jon)

print ("22222222")
jon["build"].pop('exp')
jon["build"]["exp"]["1"]=0
jon=json.dumps(jon)
print (jon)


