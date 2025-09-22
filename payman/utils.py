from typing import Type

from pydantic import BaseModel


def to_model_instance(
    source: BaseModel | dict | None, model_cls: Type[BaseModel], **overrides
) -> BaseModel:
    """
    Ensure the input is returned as an instance of the given Pydantic model.

    Args:
        source:
            - An instance of `model_cls`
            - A dictionary of field values
            - None, in which case `overrides` are used
        model_cls: The Pydantic model class to instantiate.
        overrides: Additional fields to apply if `source` is dict or None.

    Returns:
        An instance of `model_cls` with combined values.
    """

    if isinstance(source, model_cls):
        return source

    payload: dict = {}
    if isinstance(source, dict):
        payload.update(source)
    payload.update(overrides)

    return model_cls.model_validate(payload)
