from typing import Any, Dict, List, Literal

from aiotrino.auth import BasicAuthentication as BasicAuth
from aiotrino.dbapi import Connection, Cursor, connect
from opal_common.fetcher.events import FetcherConfig, FetchEvent
from opal_common.fetcher.fetch_provider import BaseFetchProvider
from pydantic import BaseModel, Field


class TrinoConnectionConfig(BaseModel):
    port: int = Field(..., description="Trino port")
    user: str = Field(..., description="Trino user")
    password: str = Field(..., description="Trino password")
    http_scheme: str = Field("http", description="Trino http scheme")
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
    config: TrinoFetcherConfig = None  # type: ignore


class TrinoFetchProvider(BaseFetchProvider):
    def __init__(self, event: TrinoFetchEvent):
        super().__init__(event)
        self._conn: Connection | None = None
        self._curr: Cursor | None = None

    def parse_event(self, event: FetchEvent) -> TrinoFetchEvent:
        return TrinoFetchEvent(**event.dict(exclude={"config"}), config=event.config)

    async def __aenter__(self):
        if self._event.config is None:
            raise RuntimeError("Config is not initialized")
        if self._event.config.connection_params.http_scheme == "http":
            self._conn = connect(
                host=self._event.url,
                port=self._event.config.connection_params.port,
                user=self._event.config.connection_params.user,
                catalog=self._event.config.connection_params.catalog,
                source=self._event.config.connection_params.source,
            )
        else:
            self._conn = connect(
                host=self._event.url,
                port=self._event.config.connection_params.port,
                user=self._event.config.connection_params.user,
                catalog=self._event.config.connection_params.catalog,
                source=self._event.config.connection_params.source,
                auth=BasicAuth(
                    username=self._event.config.connection_params.user,
                    password=self._event.config.connection_params.password,
                ),
            )
        self._curr = await self._conn.cursor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._curr:
            await self._curr.close()
        if self._conn:
            await self._conn.close()

    async def _fetch_(self) -> List[List[Any]] | List[Any]:
        if self._curr is None:
            raise RuntimeError("Cursor is not initialized")

        await self._curr.execute(self._event.config.query)

        if self._event.config.fetch_one:
            row = await self._curr.fetchone()
            if row is None:
                return []
            return row
        rows = await self._curr.fetchall()
        return rows

    async def _process_(
        self, records: List[List[Any]] | List[Any]
    ) -> List[Dict[str, Any]] | Dict[str, Any]:
        if self._curr is None or self._curr.description is None:
            raise RuntimeError("Cursor is not initialized")
        elif self._event.config.fetch_one:
            records = [records]
        columns = [desc[0] for desc in self._curr.description]
        if self._event.config.fetch_key is None:
            return [dict(zip(columns, row)) for row in records]
        index_in_columns = columns.index(self._event.config.fetch_key)
        return {row[index_in_columns]: dict(zip(columns, row)) for row in records}
