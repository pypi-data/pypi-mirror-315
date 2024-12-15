from typing import Any, List, Literal, Dict
from pydantic import BaseModel, Field

from opal_common.fetcher.fetch_provider import BaseFetchProvider
from opal_common.fetcher.events import FetcherConfig, FetchEvent

from aiotrino.dbapi import connect, Connection, Cursor


class TrinoConnectionConfig(BaseModel):
    host: str = Field(..., description="Trino host")
    port: int = Field(..., description="Trino port")
    user: str = Field(..., description="Trino user")
    password: str = Field(..., description="Trino password")
    catalog: str | None = Field(None, description="Trino catalog")
    source: str = Field("OPAL", description="Trino source")
    auth: Literal["BasicAuthentication"] = Field(
        "BasicAuthentication", description="Trino auth"
    )


class TrinoFetcherConfig(FetcherConfig):
    fetcher: str = "TrinoFetchProvider"
    connection_params: TrinoConnectionConfig = Field(
        ..., description="Trino connection parameters"
    )
    query: str = Field(..., description="Trino query")
    fetch_one: bool = Field(False, description="Fetch only one row")
    fetch_key: str | None = Field(
        None,
        description="a key of which to transform the data to object instead of array/list",
    )


class TrinoFetchEvent(FetchEvent):
    fetcher: str = "TrinoFetchProvider"
    config: TrinoFetcherConfig = Field(..., description="Trino fetcher config")

class TrinoFetchProvider(BaseFetchProvider):
    def __init__(self, event: TrinoFetchEvent):
        self._event = event
        self.__conn: Connection | None = None
        self.__curr: Cursor | None = None

    async def fetch_event(self, event: FetchEvent) -> TrinoFetchEvent:
        return TrinoFetchEvent(**event.dict())
    
    async def __aenter__(self):
        if self._event.config is None:
            raise RuntimeError("Config is not initialized")
        self.__conn = connect(
            host=self._event.config.connection_params.host,
            port=self._event.config.connection_params.port,
            user=self._event.config.connection_params.user,
            password=self._event.config.connection_params.password,
            catalog=self._event.config.connection_params.catalog,
            source=self._event.config.connection_params.source,
            auth=self._event.config.connection_params.auth,
        )
        self.__curr = await self.__conn.cursor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.__curr:
            await self.__curr.close()
        if self.__conn:
            await self.__conn.close()

    async def _fetch_(self) -> List[List[Any]] | List[Any]:
        if self.__curr is None:
            raise RuntimeError("Cursor is not initialized")
        elif self._event.config.fetch_one: 
            row = await self.__curr.fetchone()
            if row is None:
                return []
            return row
        rows = await self.__curr.fetchall()
        return rows
    
    async def _process_(self, records: List[List[Any]] | List[Any]) -> List[Dict[str, Any]] | Dict[str, Any]:
        if self.__curr is None or self.__curr.description is None:
            raise RuntimeError("Cursor is not initialized")
        elif self._event.config.fetch_one:
            records = [records]
        columns = [desc[0] for desc in self.__curr.description]
        if self._event.config.fetch_key is None:
            return [dict(zip(columns, row)) for row in records]
        index_in_columns = columns.index(self._event.config.fetch_key)
        return {row[index_in_columns]: dict(zip(columns, row)) for row in records}