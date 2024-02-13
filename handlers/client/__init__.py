from aiogram import Router

from . import homeworks, get_scores


def register_routers():
	router = Router(name='Client routers')
	router.include_routers(
		homeworks.router,
		get_scores.router,
	)
	return router


__all__ = [
	'homeworks',
	'get_scores',
]