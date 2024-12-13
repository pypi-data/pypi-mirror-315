# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class FullName(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.commons import FullName

    FullName(
        first_name="John",
        middle_name="Quincy",
        last_name="Adams",
        suffix="Jr.",
    )
    """

    first_name: str = pydantic.Field(alias="firstName")
    middle_name: typing.Optional[str] = pydantic.Field(alias="middleName", default=None)
    last_name: str = pydantic.Field(alias="lastName")
    suffix: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
