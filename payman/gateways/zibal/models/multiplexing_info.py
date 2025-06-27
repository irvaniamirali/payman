from pydantic import BaseModel, Field, ConfigDict, conint, model_validator
from pydantic.alias_generators import to_camel


class MultiplexingInfo(BaseModel):
    amount: conint(gt=0)
    bank_account: str = None
    sub_merchant_id: str = None
    wallet_id: str = None
    wage_payer: bool = None

    @model_validator(mode="after")
    def at_least_one_target(cls, values):
        if not any([values.bank_account, values.sub_merchant_id, values.wallet_id]):
            raise ValueError(
                "At least one of 'bank_account', 'sub_merchant_id', or 'wallet_id' must be provided."
            )
        return values

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
