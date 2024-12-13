# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from ...commons.types.full_name import FullName
import typing
from ...commons.types.phone_number import PhoneNumber
import pydantic
from ...commons.types.address import Address
from ...commons.types.birth_date import BirthDate
from ...commons.types.individual_government_id import IndividualGovernmentId
from .responsibilities import Responsibilities
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class RepresentativeRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.commons import (
        Address,
        BirthDate,
        FullName,
        IndividualGovernmentId,
        PhoneNumber,
    )
    from mercoa.entity_types import RepresentativeRequest, Responsibilities

    RepresentativeRequest(
        name=FullName(
            first_name="John",
            middle_name="Quincy",
            last_name="Adams",
            suffix="Jr.",
        ),
        phone=PhoneNumber(
            country_code="1",
            number="4155551234",
        ),
        email="john.doe@acme.com",
        address=Address(
            address_line_1="123 Main St",
            address_line_2="Unit 1",
            city="San Francisco",
            state_or_province="CA",
            postal_code="94105",
            country="US",
        ),
        birth_date=BirthDate(
            day="1",
            month="1",
            year="1980",
        ),
        government_id=IndividualGovernmentId(
            ssn="123-45-6789",
        ),
        responsibilities=Responsibilities(
            is_owner=True,
            ownership_percentage=40,
            is_controller=True,
        ),
    )
    """

    name: FullName
    phone: typing.Optional[PhoneNumber] = pydantic.Field(default=None)
    """
    Either phone or email is required.
    """

    email: typing.Optional[str] = pydantic.Field(default=None)
    """
    Either phone or email is required.
    """

    address: Address
    birth_date: BirthDate = pydantic.Field(alias="birthDate")
    government_id: IndividualGovernmentId = pydantic.Field(alias="governmentID")
    responsibilities: Responsibilities

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
