import pytest
from src.validate import validate_messages, validate_generation_options
from src.errors import SDKValidationError
from src.types import Message, GenerationOptions


def test_validate_messages_empty():
    with pytest.raises(SDKValidationError):
        validate_messages([])


def test_validate_messages_invalid_role():
    # Construct a Message with an invalid role at runtime
    msg = Message(role="bot", content="hello")  # type: ignore[arg-type]
    with pytest.raises(SDKValidationError):
        validate_messages([msg])


def test_validate_options_invalid_values():
    with pytest.raises(SDKValidationError):
        validate_generation_options(GenerationOptions(max_tokens=0))

    with pytest.raises(SDKValidationError):
        validate_generation_options(GenerationOptions(temperature=-1.0))
