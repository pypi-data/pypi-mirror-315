# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class TransactionFailureReason(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.transaction import TransactionFailureReason

    TransactionFailureReason(
        code="R01",
        description="The source bank account does not have sufficient funds",
    )
    """

    code: typing.Optional[str] = pydantic.Field(default=None)
    """
    The failure reason code.
    """

    description: typing.Optional[str] = pydantic.Field(default=None)
    """
    The failure reason description.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
