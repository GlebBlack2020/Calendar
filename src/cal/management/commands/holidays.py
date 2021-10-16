from django.core.management.base import BaseCommand
from ics import Calendar
from requests import get
from cal.models import Country, Holidays
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
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