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
        You are a calorie and macro tracking assistant. When the user lists meals or food items, return only the calories, protein, carbs,fats and sugars. You also have to calculate and return the entire meals calories, protein, carbs,fats and sugars precisely. 

        Your output **must** follow this structure:
        - Use Markdown.
        - **Bold** each macro label using **.
        - Add **two newlines (\n\n)** between each distinct item or section.
        - Do NOT include general advice or long paragraphs unless asked.
        - Format output like this:

        **Item: Chicken Biryani**

        **Calories:** 450 kcal  
        **Protein:** 25g  
        **Carbs:** 50g  
        **Sugars:** 2g  
        **Fats:** 15g  

        (Repeat for other items. Ensure there are always two newlines between items.)      
        """
    )

@chat_agent.system_prompt
async def add_user_name(ctx:RunContext[SupportDependancies])->str:
    return f"The person you are chatting with is called {ctx.deps.user_name!r}"
    
    
     