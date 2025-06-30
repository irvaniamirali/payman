from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class InquiryRequest(BaseModel):
    track_id: int = Field(..., description="Transaction ID")

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
