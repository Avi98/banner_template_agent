from browser.crawl_freepik import FreepikCrawler
from langchain_core.tools import tool


@tool(
	response_format="content_and_artifact",
	description="Crawl to fetch banner links for given festival and occasion",
)
async def crawl_to_fetch_banner_links(festival_name: str, occasion: str):
	"""
	Crawl to fetch banner links for festival
	Args:
		festival_name(str): name of the festival for retrieving banner
		occasion(str): name of the occasion
	Returns:
		res( dict[str, list[str]]): dict of with key as {festival_name}_{occasion}  and value as list of banner urls
	"""
	print(f"crawl_to_fetch_banner_links called with {festival_name=}, {occasion=}")

	async with FreepikCrawler(headless=False, delay=2) as crawler:
		results = await crawler.crawl_search(
			festival_name,
			occasion,
		)
		print(f"Found {sum(len(v) for v in results.values())} images")

		# if results:
		# 	print("\nFirst result:")
		# 	for key, value in results.values():
		# 		print(f"{key}: {value}")

		raw_output_dict = results
		return ("Here are the banner links for the festival.", raw_output_dict)
