# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .document_type import DocumentType
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class DocumentResponse(UniversalBaseModel):
    """
    Examples
    --------
    from mercoa.commons import DocumentResponse

    DocumentResponse(
        id="doc_37e6af0a-e637-48fd-b825-d6947b38c4e2",
        mime_type="application/pdf",
        uri="https://mercoa.com/pdf/not-real.pdf",
        type="INVOICE",
    )
    """

    id: typing.Optional[str] = pydantic.Field(default=None)
    """
    ID of the document. If not provided, this is a dynamic document that is generated on the fly.
    """

    mime_type: str = pydantic.Field(alias="mimeType")
    type: DocumentType
    uri: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
