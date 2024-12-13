# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class OcrCustomizationRequest(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import OcrCustomizationRequest

    OcrCustomizationRequest(
        line_items=True,
        invoice_metadata=True,
        line_item_metadata=True,
        line_item_gl_account_id=True,
        predict_metadata=True,
        tax_and_shipping_as_line_items=True,
    )
    """

    line_items: typing.Optional[bool] = pydantic.Field(alias="lineItems", default=None)
    """
    Extract line items from the invoice. Defaults to true.
    """

    invoice_metadata: typing.Optional[bool] = pydantic.Field(alias="invoiceMetadata", default=None)
    """
    Pull custom metadata at the invoice level. Defaults to true.
    """

    line_item_metadata: typing.Optional[bool] = pydantic.Field(alias="lineItemMetadata", default=None)
    """
    Pull custom metadata at the line item level. Defaults to true.
    """

    line_item_gl_account_id: typing.Optional[bool] = pydantic.Field(alias="lineItemGlAccountId", default=None)
    """
    Pull GL Account ID at the line item level. Defaults to true.
    """

    predict_metadata: typing.Optional[bool] = pydantic.Field(alias="predictMetadata", default=None)
    """
    Use AI to predict metadata from historical data. Defaults to true.
    """

    tax_and_shipping_as_line_items: typing.Optional[bool] = pydantic.Field(
        alias="taxAndShippingAsLineItems", default=None
    )
    """
    Pull tax and shipping information as line items. Defaults to true. If false, tax and shipping will extracted as invoice level fields.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
