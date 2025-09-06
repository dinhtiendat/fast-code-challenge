from apscheduler.schedulers.background import BackgroundScheduler

bg_scheduler = BackgroundScheduler(job_defaults={'misfire_grace_time': 3600, 'coalesce': True})