from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from ..config import settings
from pydantic import BaseModel
    
class NutritionOutput(BaseModel):
    calories:float
    protein:float
    carbs:float
    sugar:float    
    fats:float
    
gemini_model=GeminiModel(
    model_name='gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key=settings.GEMINI_API_KEY)
)

nutrition_summary_agent=Agent(
    model=gemini_model,
    output_type=NutritionOutput,
    system_prompt="""
        You are a nutrition tracking assistant.

        Your task is to analyze all messages exchanged between the AI assistant and the user for a particular day. These messages include meal logs, food items, corrections, or clarifications made by the user.

        Your job is to **calculate the final total nutrition intake** for the day, considering:

        - calories (kcal)
        - protein (g)
        - carbohydrates (g)
        - fats (g)
        - sugar (g)

        ### Important Rules:

        1. If the user makes a correction like "Actually, I had X instead of Y", or "nvm I didn’t have that", you must exclude the earlier food from totals.
        2. Only include the most recent and accurate version of any item.
        3. Skip vague or uncertain items unless a reasonable estimate can be made.
        4. Return only the final **daily total** of all meals combined.
        5. Your response must strictly match the structure of the schema provided — do not return explanations or paragraphs.

        """
    )


    
    
     