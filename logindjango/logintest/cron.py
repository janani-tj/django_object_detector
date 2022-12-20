from .models import Video
import datetime
def my_cron_job():
    start_date = datetime.date.today() - datetime.timedelta(days=10)
    Video.objects.filter(time__gte=start_date, time__lt = datetime.date.today()).delete()