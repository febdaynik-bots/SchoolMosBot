from .sync.homework import CustomHomework
from .sync.marks import CustomMarks
from .sync.rating import Rating

# Асинхронные методы лучше доставать через .dnevnik.async.


__all__ = [
	'CustomHomework',
	'CustomMarks',
	'Rating',
]
