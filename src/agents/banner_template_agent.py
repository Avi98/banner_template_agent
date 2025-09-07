import io
from PIL import Image
from langgraph.prebuilt import create_react_agent

from models import flash_lite
from browser.crawl_tool import crawl_to_fetch_banner_links
from tools.get_banner_template import (
	generate_prompt_for_template_banner,
	PromptArgs as generate_arg,
)


class BannerTemp:
	def __init__(self) -> None:
		self.agent = None

	def init_agent(self) -> "BannerTemp":
		agent = create_react_agent(
			model=flash_lite,
			tools=[
				crawl_to_fetch_banner_links,
			],
		)

		self.agent = agent
		return self

	async def init_prompt_generation(self, generate_arg: generate_arg) -> "BannerTemp":
		(m, response) = await generate_prompt_for_template_banner.ainvoke(
			input={
				"args": generate_arg,
			}
		)
		return response

	async def invoke_agent(self, prompt):
		assert self.agent, "Can not invoke agent without initializing"

		return await self.agent.ainvoke(prompt)

	def show_graph(
		self,
	) -> None:
		assert self.agent, "Can not invoke agent without initializing"

		png_data = self.agent.get_graph().draw_mermaid_png()

		img_bytes = io.BytesIO(png_data)
		image = Image.open(img_bytes)

		image.show()
