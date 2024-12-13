# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .entity_id import EntityId
import pydantic
from .counterparty_customization_request import CounterpartyCustomizationRequest
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class EntityAddPayeesRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import (
        CounterpartyCustomizationAccount,
        CounterpartyCustomizationRequest,
        EntityAddPayeesRequest,
    )

    EntityAddPayeesRequest(
        payees=["ent_21661ac1-a2a8-4465-a6c0-64474ba8181d"],
        customizations=[
            CounterpartyCustomizationRequest(
                counterparty_id="ent_21661ac1-a2a8-4465-a6c0-64474ba8181d",
                accounts=[
                    CounterpartyCustomizationAccount(
                        account_id="85866843",
                        postal_code="94105",
                        name_on_account="John Doe",
                    )
                ],
            )
        ],
    )
    """

    payees: typing.List[EntityId] = pydantic.Field()
    """
    List of payee entity IDs or foreign IDs to associate with the entity
    """

    customizations: typing.Optional[typing.List[CounterpartyCustomizationRequest]] = pydantic.Field(default=None)
    """
    List of customizations to apply to the payees. If the payee is not currently a counterparty of the entity, the counterparty will be created with the provided customizations.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
