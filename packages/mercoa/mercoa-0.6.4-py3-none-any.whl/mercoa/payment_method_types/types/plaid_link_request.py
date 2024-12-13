# This file was auto-generated by Fern from our API Definition.

import typing
from .plaid_processor_token_request import PlaidProcessorTokenRequest
from .plaid_public_token_request import PlaidPublicTokenRequest
from .plaid_access_token_request import PlaidAccessTokenRequest

PlaidLinkRequest = typing.Union[PlaidProcessorTokenRequest, PlaidPublicTokenRequest, PlaidAccessTokenRequest]
