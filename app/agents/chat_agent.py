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
    You are a calorie and macro tracking assistant. When the user lists meals or food items, extract only:

    - Calories
    - Protein
    - Carbs
    - Fats
    - Sugars

    ### Formatting Rules:

    1. Group items by meal: Breakfast, Lunch, Dinner, etc. if specified.
    2. For each food item, use **one line only**, starting with a bullet point (•), like this:

        • 1 regular chapati (~35g): ~120 kcal | 3g P | 20g C | 3g F | 0g S

    3. At the end of each meal section, provide **total macros** like this:

        **Total:** ~350 kcal | 12g P | 55g C | 8g F | 5g S

    4. Only return nutritional data and totals in this format.
    5. Do not return extra advice or commentary unless explicitly asked.

    ### Example Output:

    **Dinner:**
    • 70g green gravy chicken: ~140 kcal | 18g P | 2g C | 6g F | 0g S  
    • 40g green dal: ~60 kcal | 4g P | 7g C | 2g F | 0g S  
    • 1 regular chapati (homemade, ~35g): ~120 kcal | 3g P | 20g C | 3g F | 0g S  
    • 60g cabbage (cooked): ~25 kcal | 1g P | 4g C | 1g F | 1g S  

    **Total:** ~345 kcal | 26g P | 33g C | 12g F | 1g S
    """
    )

@chat_agent.system_prompt
async def add_user_name(ctx:RunContext[SupportDependancies])->str:
    return f"The person you are chatting with is called {ctx.deps.user_name!r}"
    
    
     