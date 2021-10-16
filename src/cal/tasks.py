import pytz
from django.core.mail import send_mail
from .models import CreateEvent, Country, Holidays
from datetime import datetime, timedelta
from ics import Calendar
from requests import get
from tqdm import tqdm
from celery import shared_task


@ shared_task
def check_send_email():
    now_time = pytz.UTC.localize(datetime.now())
    events = CreateEvent.objects.all()
    for event in events:
        if event.notification:
            list_time = event.reminder.split(':')
            if len(list_time[0]) == 1:
                time_delta = timedelta(hours=int(list_time[0]))
            else:
                list_dey = list_time[0].split(' ')
                time_delta = timedelta(days=int(list_dey[0]))
            if event.date_start - time_delta < now_time + timedelta(hours=3):
                email = event.user_event.email
                send_mail("It's your Planned event",
                          f"Event:{event.title}, Time:{event.date_start}",
                          "glebblack2020@gmail.com", [email])
                event.notification = False
                event.save()
    return 'Done'


@ shared_task
def list_of_holidays():
    Holidays.objects.all().delete()
    for country in tqdm(Country.objects.all()):
        url = f"https://www.officeholidays.com/ics/{country.country}"
        try:
            cal1 = Calendar(get(url).text)
        except:
            pass
        for holiday in cal1.events:
            try:
                Holidays.objects.create(title=holiday.name,
                                        holiday_start=holiday.begin.format("YYYY-MM-DD HH:mm:ss"),
                                        holiday_finish=holiday.end.format("YYYY-MM-DD HH:mm:ss"),
                                        country=country)
            except Exception as exc:
                print(exc)
                pass