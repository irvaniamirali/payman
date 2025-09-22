from pydantic import BaseModel

from payman.utils import to_model_instance


class DummyModel(BaseModel):
    x: int
    y: str = "default"


def test_to_model_instance_from_model():
    obj = DummyModel(x=1, y="a")
    result = to_model_instance(obj, DummyModel)
    assert result is obj


def test_to_model_instance_from_dict():
    result = to_model_instance({"x": 2}, DummyModel)
    assert isinstance(result, DummyModel)
    assert result.x == 2
    assert result.y == "default"


def test_to_model_instance_with_overrides():
    result = to_model_instance({"x": 3}, DummyModel, y="override")
    assert result.y == "override"


def test_to_model_instance_from_none_with_overrides():
    result = to_model_instance(None, DummyModel, x=10, y="hey")
    assert result.x == 10
    assert result.y == "hey"
