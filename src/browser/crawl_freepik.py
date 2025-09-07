from typing import Any, List, Dict
import asyncio
import logging
from urllib.parse import urlencode
from playwright.async_api import async_playwright

logging.basicConfig(
	level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FreepikCrawler:
	def __init__(self, headless: bool = True, delay: int = 2):
		"""
		Initialize the Freepik crawler

		Args:
		    headless (bool): Run browser in headless mode
		    delay (int): Delay between requests in seconds
		"""
		self.headless = headless
		self.delay = delay
		self.browser = None
		self.page = None

	async def __aenter__(self):
		"""Async context manager entry"""
		self.playwright = await async_playwright().start()
		self.browser = await self.playwright.chromium.launch(
			headless=self.headless, args=["--no-sandbox", "--disable-dev-shm-usage"]
		)
		context = await self.browser.new_context()

		self.page = await context.new_page()

		self.page

		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):  # type: ignore
		"""Async context manager exit"""
		if self.browser:
			await self.browser.close()
		if hasattr(self, "playwright"):
			await self.playwright.stop()

	def build_url(
		self, query: str, dynamic_value: str, template_type: str = "template"
	) -> str:
		"""
		Build Freepik search URL with dynamic parameters

		Args:
		    query (str): Search query (e.g., "dewali")
		    dynamic_value (str): Dynamic value for last_value parameter
		    template_type (str): Type of content to search for

		Returns:
		    str: Complete URL
		"""
		base_url = "https://www.freepik.com/search"
		params = {
			"format": "search",
			"last_filter": "query",
			"last_value": dynamic_value,
			"query": query,
			"type": template_type,
		}

		return f"{base_url}?{urlencode(params)}"

	async def wait_for_content(self, timeout: int = 10000):
		"""Wait for content to load"""
		try:
			assert self.page is not None, "Page not found"

			await self.page.wait_for_selector(
				'[data-testid="search-result"]', timeout=timeout
			)

			logger.info("Search results loaded successfully")
		except Exception as e:
			logger.warning(f"Timeout waiting for search results: {e}")
			# Continue anyway, sometimes content loads without the expected selector

	async def extract_image_data(self) -> dict[str, list[str]]:
		"""
		Extract image data from the current page

		Returns:
		    List[Dict]: List of dictionaries containing image information
		"""
		images = None

		try:
			assert self.page, "Page not found in extract_image_data"

			await self.page.wait_for_timeout(3000)

			links = self.page.locator('img[src*="img.freepik.com"]')

			count = await links.count()

			if count == 0:
				raise Exception("No banner image found")

			html = await self.page.content()
			print("img.freepik.com" in html)

			img_src_list: list[str] = await links.evaluate_all(
				"(elements) => elements.map(el => el.src)"
			)

			images = {"product_banner_url": [url for url in img_src_list][:2]}

		#     for element in image_elements:
		#         try:
		#             image_data = {}

		#             # Extract image URL
		#             img_element = await element.query_selector('img')
		#             if img_element:
		#                 image_data['image_url'] = await img_element.get_attribute('src')
		#                 image_data['alt_text'] = await img_element.get_attribute('alt')

		#             # Extract title/description
		#             title_element = await element.query_selector('[data-testid="resource-title"]')
		#             if title_element:
		#                 image_data['title'] = await title_element.text_content()

		#             # Extract resource link
		#             link_element = await element.query_selector('a')
		#             if link_element:
		#                 href = await link_element.get_attribute('href')
		#                 if href:
		#                     image_data['resource_url'] = f"https://www.freepik.com{href}" if href.startswith('/') else href

		#             # Extract premium status
		#             premium_element = await element.query_selector('[data-testid="premium-badge"]')
		#             image_data['is_premium'] = premium_element is not None

		#             # Extract author info if available
		#             author_element = await element.query_selector('.author')
		#             if author_element:
		#                 image_data['author'] = await author_element.text_content()

		#             if image_data.get('image_url'):
		#                 images.append(image_data)

		#         except Exception as e:
		#             logger.warning(f"Error extracting data from image element: {e}")
		#             continue

		except Exception as e:
			logger.error(f"Error extracting image data: {e}")
			raise e

		logger.info("Extracted product links from current page")
		return images

	async def crawl_search(
		self,
		query: str,
		dynamic_value: str,
	):
		all_images = {}

		try:
			url = self.build_url(query, dynamic_value)

			assert self.page, "Page not found in crawl_search"

			await self.page.goto(url, wait_until="networkidle")
			await self.wait_for_content()

			page_images = await self.extract_image_data()
			all_images = page_images

			await asyncio.sleep(self.delay)

		except Exception as e:
			logger.error(f"Error crawling page : {e}")

		return all_images
