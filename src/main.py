#!/usr/bin/env python3

import asyncio
from dotenv import load_dotenv
from agents.banner_template_agent import BannerTemp

load_dotenv()

if __name__ == "__main__":
	print("started logging")
	# asyncio.run(
	# 	crawl_to_fetch_banner_links.ainvoke(
	# 		{"festival_name": "dewali", "occasion": "festival"}
	# 	)
	# )
	bannerTemp = BannerTemp()
	agent = bannerTemp.init_agent()

	result = asyncio.run(
		agent.invoke_agent(
			{
				"messages": [
					{
						"role": "user",
						"content": "Crawl to fetch banner links, for festival :- dewali, occasion:- festival.",
					}
				]
			}
		)
	)

	for message in result["messages"]:
		# Look for the tool message named 'crawl_to_fetch_banner_links'
		if message.get("name") == "crawl_to_fetch_banner_links":
			artifact = message.get("artifact", {})
			urls = artifact.get("product_banner_url", [])
			print("Banner URLs:", urls)

	print(result)
	# agent.show_graph()
