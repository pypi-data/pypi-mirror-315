import json
import logging
from typing import Type

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from duck_agents.llm.session_factory import SessionFactory

_logger = logging.getLogger(__name__)

_system_prompt_template = (
    "{task_description}\n"
    "The user will provide the input for your task in structured JSON format."  
    "The input adheres to the following JSON schema:\n"
    "{input_schema}"
)

class BaseAgent:
    def __init__(
            self,
            llm_session_factory: SessionFactory,
            task_description: str,
            input_schema: Type[BaseModel],
            output_schema: Type[BaseModel]):

        self.llm_session_factory = llm_session_factory
        self.input_schema = input_schema
        self.task_description = task_description
        input_schema_json = json.dumps(self.input_schema.model_json_schema())
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", _system_prompt_template),
                ("user", "{data}")
            ]
        )
        self.llm_session = self.llm_session_factory.create_session(output_schema=output_schema)
        self.chain = self.prompt_template | self.llm_session
        self.agent_type = type(self).__name__


    def prompt(self, data: BaseModel) -> BaseModel:
        return self.chain.invoke(
            {
                "data": data.model_dump_json(),
                "task_description": self.task_description,
                "input_schema": self.input_schema.model_json_schema()
            }
        )