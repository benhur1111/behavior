from anthropic import Anthropic
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return message.content[0].text
