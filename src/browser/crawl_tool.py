from browser.crawl_freepik import FreepikCrawler
from langchain_core.tools import tool


@tool
async def crawl_to_fetch_banner_links(festival_name: str, occasion: str):
	"""
	Crawl to fetch banner links
	Args:
		festival_name(str): name of the festival for retrieving banner
		occasion(str): name of the occasion
	Returns:
		res( dict[str, list[str]]): dict of with key as {festival_name}_{occasion}  and value as list of banner urls
	"""
	async with FreepikCrawler(headless=False, delay=2) as crawler:
		results = await crawler.crawl_search(festival_name, occasion, max_pages=1)
		print(f"Found {len(results.values())} images")

		# if results:
		# 	print("\nFirst result:")
		# 	for key, value in results.values():
		# 		print(f"{key}: {value}")

		return results
