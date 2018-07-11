from apscheduler.schedulers.blocking import BlockingScheduler
from task2 import my_tasks_cron
from hour_tasks import hour_tasks_cron

sched = BlockingScheduler()
'''
@sched.scheduled_job('interval', minutes=1)
def print_data():
	print("Have a good day!")
'''
@sched.scheduled_job('interval', minutes=1)
def update_a():
 #	my_tasks_cron()

@sched.scheduled_job('interval', hours=1)
def update_b():
 	hour_tasks_cron()

sched.start()