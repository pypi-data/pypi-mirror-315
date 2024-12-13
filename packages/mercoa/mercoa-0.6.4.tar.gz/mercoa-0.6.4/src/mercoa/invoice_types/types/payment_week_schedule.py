# This file was auto-generated by Fern from our API Definition.

from .payment_schedule_base import PaymentScheduleBase
import typing
from .day_of_week import DayOfWeek
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PaymentWeekSchedule(PaymentScheduleBase):
    """
    Examples
    --------
    import datetime

    from mercoa.invoice_types import PaymentWeekSchedule

    PaymentWeekSchedule(
        repeat_on=["1", "3", "5"],
        ends=datetime.datetime.fromisoformat(
            "2021-01-01 00:00:00+00:00",
        ),
    )
    """

    repeat_on: typing.List[DayOfWeek] = pydantic.Field(alias="repeatOn")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
