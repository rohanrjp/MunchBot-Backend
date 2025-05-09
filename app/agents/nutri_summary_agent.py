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

        Your task is to analyze all messages exchanged between the AI assistant and the user for a particular day. These messages may include the user's meal logs, foods consumed, AI replies, or nutritional information.

        From the entire conversation, extract the total nutrition intake for that day. Return a single combined total across all meals for:

        - calories (in kcal)
        - protein (grams)
        - carbohydrates (grams)
        - fats (grams)
        - sugar (grams)

        Only consider entries that clearly mention food intake or quantities. If quantities are vague, make reasonable estimations.

        Strictly return only the structured output as specified in the schema. Do not add any explanation or extra text.    
        """
    )


    
    
     