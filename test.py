import time
from pprint import pprint
import datetime

print(time.ctime())
now=time.time()
now+=660
print(time.ctime(now))
now = datetime.datetime.now() 
print(now)