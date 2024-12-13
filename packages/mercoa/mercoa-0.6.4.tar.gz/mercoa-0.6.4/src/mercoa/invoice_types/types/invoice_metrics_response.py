# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...payment_method_types.types.currency_code import CurrencyCode
from .invoice_metrics_per_date_response import InvoiceMetricsPerDateResponse
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class InvoiceMetricsResponse(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from mercoa.invoice_types import (
        InvoiceMetricsPerDateResponse,
        InvoiceMetricsResponse,
    )

    InvoiceMetricsResponse(
        total_amount=1000.0,
        total_count=10,
        average_amount=100.0,
        currency="USD",
        dates={
            "2021-01-01T00:00:00Z": InvoiceMetricsPerDateResponse(
                date=datetime.datetime.fromisoformat(
                    "2021-01-01 00:00:00+00:00",
                ),
                total_amount=100.0,
                total_count=1,
                average_amount=100.0,
                currency="USD",
            ),
            "2021-01-02T00:00:00Z": InvoiceMetricsPerDateResponse(
                date=datetime.datetime.fromisoformat(
                    "2021-01-02 00:00:00+00:00",
                ),
                total_amount=200.0,
                total_count=2,
                average_amount=100.0,
                currency="USD",
            ),
            "2021-01-03T00:00:00Z": InvoiceMetricsPerDateResponse(
                date=datetime.datetime.fromisoformat(
                    "2021-01-03 00:00:00+00:00",
                ),
                total_amount=400.0,
                total_count=2,
                average_amount=200.0,
                currency="USD",
            ),
        },
    )
    """

    group: typing.Optional[typing.List[typing.Dict[str, str]]] = pydantic.Field(default=None)
    """
    If groupBy is provided, this will be the group by value.
    """

    total_amount: float = pydantic.Field(alias="totalAmount")
    total_count: int = pydantic.Field(alias="totalCount")
    average_amount: float = pydantic.Field(alias="averageAmount")
    currency: CurrencyCode
    dates: typing.Optional[typing.Dict[str, InvoiceMetricsPerDateResponse]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
