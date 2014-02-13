from crontab import CronTab

cron  = CronTab(user=True)

def Add(cmd, t, id):
	job = cron.new(command=cmd, comment=id)
