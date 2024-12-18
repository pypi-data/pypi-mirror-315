from dataclasses import dataclass, field
import asyncio

from .._types._huggingface import HFModelType
from ...customs.main import HFAgent


@dataclass
class AgentTask:
    query: str
    system_prompt: str = field(default="")
    model: HFModelType = field(default="huggingface:Qwen/Qwen2.5-72B-Instruct")
    model_args: dict = field(default_factory=lambda: {"temperature": 0})


class AgentPool:
    def __init__(self,
                 model:HFModelType|None=None,
                 system_prompt:str|None=None,
                 max_concurrent: int = 10,
                 agent_model= None):
        self._agents = {}
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self.agent_pool_model:HFModelType = model
        self.agent_pool_system_prompt = system_prompt
        self.agent_model = agent_model or HFAgent

    async def _controlled_query(self, task: AgentTask):
        async with self._semaphore:
            try:
                agent_key = f"{task.model}_{task.system_prompt}"

                if agent_key not in self._agents:
                    self._agents[agent_key] = self.agent_model(self.agent_pool_model or task.model,
                                                      **task.model_args)(self.agent_pool_system_prompt or task.system_prompt)

                response = await self._agents[agent_key](task.query)
                return response
            except Exception as e:
                return f"Error: {str(e)}"

    async def _process_batch(self, tasks: list[AgentTask]) -> list:
        tasks = [AgentTask(query=t) if isinstance(t,str) else t for t in tasks]
        tasks_to_run = [self._controlled_query(task) for task in tasks]
        return await asyncio.gather(*tasks_to_run)

    def run(self, tasks: list[AgentTask]| list[str]) -> list:
        """
        Process a batch of tasks and return results.
        This method handles the async event loop internally.
        """
        return asyncio.run(self._process_batch(tasks))


# Usage example:
if __name__ == "__main__":
    # tasks = [
    #     AgentTask(
    #         model="huggingface:NousResearch/Hermes-3-Llama-3.1-8B",
    #         system_prompt="You are DR suma kammmmari",
    #         query="what is 5+6?"
    #     ),
    #     AgentTask(
    #         model="huggingface:NousResearch/Hermes-3-Llama-3.1-8B",
    #         system_prompt="You are a math teacher",
    #         query="what is 4-2?"
    #     )
    # ]

    agents = AgentPool()
    results = agents.run(["2+4?","what is 4-2?"])
    print(results)