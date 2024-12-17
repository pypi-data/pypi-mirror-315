from typing import Type

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, SecretStr

from duck_agents.llm.session_factory import SessionFactory

# Assumes that either env variable GOOGLE_API_KEY is set or the api key is passed as arg
class GeminiSessionFactory(SessionFactory):
    def __init__(self, model_name, api_key: SecretStr = None):
        self.model_name = model_name
        self.api_key = api_key

    def create_session(self, output_schema: Type[BaseModel] = None, temperature: float = 0):
         kwargs = {
             "model": self.model_name,
             "temperature": temperature,
         }
         if self.api_key is not None: kwargs["google_api_key"] = self.api_key
         return ChatGoogleGenerativeAI(**kwargs).with_structured_output(schema=output_schema)