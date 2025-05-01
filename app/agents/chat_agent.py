from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from ..config import settings
from sqlalchemy.orm import Session

@dataclass
class SupportDependancies:
    user_name:str
    
gemini_model=GeminiModel(
    model_name='gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key=settings.GEMINI_API_KEY)
)

chat_agent=Agent(
    model=gemini_model,
    deps_type=SupportDependancies,
    system_prompt="Be a calorie calculating and tracking agent.The user can provide all the meals they have had during the day.Respond to these meals by telling how many calories and macros are there in each meal.Return in markdown.Always respond in Markdown format.Use bold (**text**) for emphasis, and include line breaks (\\n) between paragraphs or points.\n"
)

@chat_agent.system_prompt
async def add_user_name(ctx:RunContext[SupportDependancies])->str:
    return f"The person you are chatting with is called {ctx.deps.user_name!r}"
    
    
     