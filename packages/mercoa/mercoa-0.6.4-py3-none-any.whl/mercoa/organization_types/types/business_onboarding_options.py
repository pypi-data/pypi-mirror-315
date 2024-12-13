# This file was auto-generated by Fern from our API Definition.

from .common_onboarding_options import CommonOnboardingOptions
from .onboarding_option import OnboardingOption
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class BusinessOnboardingOptions(CommonOnboardingOptions):
    type: OnboardingOption
    doing_business_as: OnboardingOption = pydantic.Field(alias="doingBusinessAs")
    ein: OnboardingOption
    mcc: OnboardingOption
    formation_date: OnboardingOption = pydantic.Field(alias="formationDate")
    website: OnboardingOption
    description: OnboardingOption
    representatives: OnboardingOption
    logo: OnboardingOption
    average_transaction_size: OnboardingOption = pydantic.Field(alias="averageTransactionSize")
    average_monthly_transaction_volume: OnboardingOption = pydantic.Field(alias="averageMonthlyTransactionVolume")
    max_transaction_size: OnboardingOption = pydantic.Field(alias="maxTransactionSize")

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
