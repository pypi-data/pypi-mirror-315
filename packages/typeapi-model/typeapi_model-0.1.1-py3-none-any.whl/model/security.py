from pydantic import BaseModel, Field, GetCoreSchemaHandler, Tag
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Annotated, Union
from .security_api_key import SecurityApiKey
from .security_http_basic import SecurityHttpBasic
from .security_http_bearer import SecurityHttpBearer
from .security_o_auth import SecurityOAuth


class Security(BaseModel):
    type: Optional[str] = Field(default=None, alias="type")
    pass


