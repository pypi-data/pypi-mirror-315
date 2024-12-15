import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from unstructured_ingest.interfaces import  ProcessorConfig, ReadConfig
from unstructured_ingest.connector.jira import SimpleJiraConfig, JiraAccessConfig
from unstructured_ingest.runner import JiraRunner
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from pydantic import BaseModel, Field, AliasChoices
from typing import Optional, Union

class JiraParams(BaseModel):
  url: str
  access_token: str = Field(validation_alias=AliasChoices("accessToken","access_token"))
  user_email: str = Field(validation_alias=AliasChoices("userEmail","user_email"))
  projects: list[str]
  boards: Optional[list[str]] | None = None
  issues: Optional[list[str]] | None = None
class Jira(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = JiraParams.model_validate(self.data)
  def working_subdirectory(self) -> str:
    return 'jira'
  def run(self) -> None:
    access_config = JiraAccessConfig(
      api_token=self.__data.access_token
    )
    config = SimpleJiraConfig(
      user_email=self.__data.user_email,
      url = self.__data.url,
      access_config=access_config,
      projects=self.__data.projects,
      boards=self.__data.boards,
      issues=self.__data.issues
    )
    runner = JiraRunner(
      connector_config=config,
      processor_config=ProcessorConfig(reprocess=False,verbose=False,num_processes=2,raise_on_error=False),
      read_config=ReadConfig(download_dir=self.working_directory,re_download=True,preserve_downloads=True,download_only=True),
      partition_config=None,
      retry_strategy_config=None
      )
    runner.run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()
