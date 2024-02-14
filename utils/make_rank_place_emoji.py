def make_rank_place_emoji(number: int) -> str:
	symbols = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
	return ''.join(symbols[int(digit)] for digit in str(number))