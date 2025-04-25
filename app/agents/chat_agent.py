from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from ..config import settings

gemini_model=GeminiModel(
    model_name='gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key=settings.GEMINI_API_KEY)
)

chat_agent=Agent(
    model=gemini_model,
    system_prompt="Be a calorie calculating and tracking agent.The user can provide all the meals they have had during the day.Respond to these meals by telling how many calories and macros are there in each meal"
)
    