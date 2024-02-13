import datetime


async def get_week_boundaries(date: datetime.date):
	# Определяем первый день недели (понедельник)
	start_of_week = date - datetime.timedelta(days=date.weekday())

	# Определяем последний день недели (воскресенье)
	end_of_week = start_of_week + datetime.timedelta(days=6)

	return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')