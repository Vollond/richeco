import time
from pprint import pprint
import datetime
from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)
import json


print(time.ctime())
now=time.time()
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

print (jon)
jon["build"]["pim"]=0
jon=json.dumps(jon)
print (jon)