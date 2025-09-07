from pydantic import BaseModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool

from models import flash_lite


class PromptArgs(BaseModel):
	product_banner_url: list[str]
	festival_name: str


class ResponseType(BaseModel):
	festival: list[dict[int, str]]


@tool(
	response_format="content_and_artifact",
	description="Tool for generating prompts for banner template",
	args_schema=PromptArgs,
)
async def generate_prompt_for_template_banner(arg: PromptArgs):
	"""
	Generates prompts for template banner generation.
	Args:
	  arg: {product_banner_url:list[str]} :-  product_banner_url has list of all the urls with templates
	  festival_name: str
	Returns:
	    {festival_name}: [
	     1: str,
	     2: str,
	     3: str,
	     4: str,
	     5: str
	    ]
	"""

	urls, festival_name = arg.model_dump().values()
	prompt = [
		f"Analysis the banner image for the festival {festival_name}",
		"create a detailed prompt with all the elements in image placed position",
		"the prompt should remove the text from the banner template",
		"Banner image should be produced with height: 768 and width: 768.",
		"No other text or lettering.",
	]

	llm = flash_lite.with_structured_output(ResponseType)

	results = []
	for i, banner_url in enumerate(urls):
		prompt.append(f"for int key use {i}")

		response = await llm.ainvoke(
			input=[SystemMessage(content="\n".join(prompt)), {"image_data": banner_url}]
		)

		results.append(response)
	return ("Here are the prompt for generating all the banners", results)
