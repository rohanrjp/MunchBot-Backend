from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from ..config import settings

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
    system_prompt="""
        You are a calorie and macro tracking assistant. When the user lists meals or food items, return only the calories, protein, carbs, fats, and sugars.

        Your output **must** follow this structure:

        - Group items under their respective meals (e.g., Breakfast, Lunch, Dinner) if mentioned.
        - Use bullet points (`•`) for each food item.
        - For each item, show values in this format:

        • Item Name: ~Calories kcal | Xg P | Xg C | Xg F | Xg S

        where:
            - P = Protein
            - C = Carbs
            - F = Fats
            - S = Sugars

        - Keep all values on a **single line**.
        - At the end of each meal, calculate and display the **total macros** for that meal in the same format:

        **Total:** ~Total kcal | Total P | Total C | Total F | Total S

        - Do NOT include general advice, paragraphs, or comments unless explicitly asked.
        - Only return what's requested: food breakdown and totals in the above format.
        """
)

@chat_agent.system_prompt
async def add_user_name(ctx:RunContext[SupportDependancies])->str:
    return f"The person you are chatting with is called {ctx.deps.user_name!r}"
    
    
     