import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from school_mos import AUTH


async def authStudent(login: str, password: str) -> AUTH:
	loop = asyncio.get_event_loop()

	with ThreadPoolExecutor(2) as pool:
		x = loop.run_in_executor(pool, AUTH, login, password)
		result = await x
	loop.close()
	return result
