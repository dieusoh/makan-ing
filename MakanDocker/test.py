from datetime import date
import calendar

today = date.today()
print(calendar.day_name[today.weekday()])