from calendar import HTMLCalendar
from asesor.models import Event

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, hola=None):
		self.year = year
		self.month = month
		self.hola = hola
		super(Calendar, self).__init__()

	def Obten_mes(self):
		return self.month

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user__Nombre=self.hola)

		cal = f'<table style="border-spacing: 1; border-collapse: collapse; background: rgb(236, 235, 235); overflow: hidden; width: 100%; margin: 0 auto;position: relative;" border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal