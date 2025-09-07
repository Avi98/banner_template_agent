#!/usr/bin/env python3

import asyncio

from browser.crawl_tool import crawl_to_fetch_banner_links


if __name__ == "__main__":
	# results = await simple_crawl()
	print("started logging")
	asyncio.run(
		crawl_to_fetch_banner_links.ainvoke(
			{"festival_name": "dewali", "occasion": "festival"}
		)
	)
