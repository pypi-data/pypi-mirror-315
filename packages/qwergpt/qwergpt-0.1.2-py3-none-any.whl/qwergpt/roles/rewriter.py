from abc import ABC, abstractmethod

from qwergpt.pipelines.base import PipelineComponent
from qwergpt.llms import (
    ZhipuLLM,
    DeepSeekLLM,
)


class BaseRewriter(PipelineComponent):
    def __init__(self, model_name: str = 'glm-4-air'):
        self._llm = ZhipuLLM(model_name=model_name)

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def get_user_prompt_template(self) -> str:
        pass
