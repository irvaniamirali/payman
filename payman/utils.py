from typing import Type, Union
from pydantic import BaseModel


def parse_input(data: Union[BaseModel, dict, None], model: Type[BaseModel], **kwargs) -> BaseModel:
    """
    Convert input data to a Pydantic model instance.

    Args:
        data: Could be
            - instance of `model` (BaseModel subclass),
            - dict of fields,
            - or None (then kwargs is used).
        model: Pydantic model class to convert to.
        kwargs: Additional fields if data is None.

    Returns:
        instance of `model`
    """
    if isinstance(data, model):
        return data
    elif isinstance(data, dict):
        # merge dict and kwargs
        merged = {**data, **kwargs}
        return model.model_validate(merged)
    else:
        # data is None or something else, use kwargs only
        return model.model_validate(kwargs)
