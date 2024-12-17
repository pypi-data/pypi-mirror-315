from typing import Type

from langchain_ollama import OllamaLLM
from pydantic import BaseModel

from duck_agents.llm.session_factory import SessionFactory

class OLlamaSessionFactory(SessionFactory):
    def __init__(self, url: str, model_name: str):
        self.url = url
        self.model_name = model_name

    def create_session(self, output_schema: Type[BaseModel] = None, temperature: float = 0):
        # TODO: implement workaround, since OLLAMA doesn't support function calling (or langchain didn't implement it yet)
        return (OllamaLLM(model=self.model_name, temperature=temperature, base_url=self.url)
                  .with_structured_output(schema=output_schema))