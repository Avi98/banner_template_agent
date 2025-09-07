from langchain_google_genai import ChatGoogleGenerativeAI

flash_img = ChatGoogleGenerativeAI(
	model="gemini-2.5-flash-image-preview",
	temperature=0,
	max_tokens=None,
	timeout=None,
	max_retries=2,
)


flash_lite = ChatGoogleGenerativeAI(
	model="gemini-2.5-flash-lite",
	temperature=0,
	max_tokens=None,
	timeout=None,
	max_retries=2,
)
