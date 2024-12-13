# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .metadata_customization_request import MetadataCustomizationRequest
from .payment_method_customization_request import PaymentMethodCustomizationRequest
import pydantic
from .ocr_customization_request import OcrCustomizationRequest
from .notification_customization_request import NotificationCustomizationRequest
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class EntityCustomizationResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.entity_types import (
        EntityCustomizationResponse,
        MetadataCustomizationRequest,
        NotificationCustomizationRequest,
        OcrCustomizationRequest,
        PaymentMethodCustomizationRequest,
    )

    EntityCustomizationResponse(
        metadata=[
            MetadataCustomizationRequest(
                key="my_custom_field",
                disabled=True,
            ),
            MetadataCustomizationRequest(
                key="my_other_field",
                disabled=False,
            ),
        ],
        payment_source=[
            PaymentMethodCustomizationRequest(
                type="bankAccount",
                disabled=True,
            ),
            PaymentMethodCustomizationRequest(
                type="custom",
                schema_id="cpms_7df2974a-4069-454c-912f-7e58ebe030fb",
                disabled=True,
            ),
        ],
        backup_disbursement=[
            PaymentMethodCustomizationRequest(
                type="check",
                disabled=True,
            )
        ],
        payment_destination=[
            PaymentMethodCustomizationRequest(
                type="bankAccount",
                disabled=True,
            ),
            PaymentMethodCustomizationRequest(
                type="check",
                disabled=True,
            ),
        ],
        ocr=OcrCustomizationRequest(
            line_items=True,
            invoice_metadata=True,
            line_item_metadata=True,
            line_item_gl_account_id=True,
            predict_metadata=True,
            tax_and_shipping_as_line_items=True,
        ),
        notifications=NotificationCustomizationRequest(
            assume_role="admin",
        ),
    )
    """

    metadata: typing.List[MetadataCustomizationRequest]
    payment_source: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="paymentSource")
    backup_disbursement: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="backupDisbursement")
    payment_destination: typing.List[PaymentMethodCustomizationRequest] = pydantic.Field(alias="paymentDestination")
    ocr: OcrCustomizationRequest
    notifications: NotificationCustomizationRequest

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
