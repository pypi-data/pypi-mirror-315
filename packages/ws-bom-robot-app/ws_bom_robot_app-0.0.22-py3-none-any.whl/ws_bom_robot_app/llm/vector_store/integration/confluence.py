import asyncio
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.v2.processes.connectors.confluence import ConfluenceIndexerConfig, ConfluenceDownloaderConfig, ConfluenceConnectionConfig, ConfluenceAccessConfig
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Union
from pydantic import BaseModel, Field, AliasChoices

class ConfluenceParams(BaseModel):
  url: str
  access_token: str = Field(validation_alias=AliasChoices("accessToken","access_token"))
  user_email: str = Field(validation_alias=AliasChoices("userEmail","user_email"))
  spaces: list[str] = []
class Confluence(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = ConfluenceParams.model_validate(self.data)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'confluence'
  def run(self) -> None:
    indexer_config = ConfluenceIndexerConfig(
      spaces=self.__data.spaces
    )
    downloader_config = ConfluenceDownloaderConfig(
      download_dir=self.working_directory
    )
    connection_config = ConfluenceConnectionConfig(
      access_config=ConfluenceAccessConfig(api_token=self.__data.access_token),
      url=self.__data.url,
      user_email=self.__data.user_email
    )
    self.__unstructured_ingest.pipeline(
      indexer_config,
      downloader_config,
      connection_config).run()
  async def load(self) -> list[Document]:
      await asyncio.to_thread(self.run)
      await asyncio.sleep(1)
      return await Loader(self.working_directory).load()

