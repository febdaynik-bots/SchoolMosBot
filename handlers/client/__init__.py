from aiogram import Router

from . import homeworks


def register_routers():
	router = Router(name='Client routers')
	router.include_routers(
		homeworks.router,
	)
	return router


__all__ = [
	'homeworks',
]