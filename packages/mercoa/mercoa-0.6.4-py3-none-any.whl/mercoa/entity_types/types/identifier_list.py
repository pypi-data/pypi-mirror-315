# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from .entity_user_id import EntityUserId


class IdentifierList_RolesList(UniversalBaseModel):
    value: typing.List[str]
    type: typing.Literal["rolesList"] = "rolesList"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True


class IdentifierList_UserList(UniversalBaseModel):
    value: typing.List[EntityUserId]
    type: typing.Literal["userList"] = "userList"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True


IdentifierList = typing.Union[IdentifierList_RolesList, IdentifierList_UserList]
