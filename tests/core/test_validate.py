import pytest
from imrabo_ai_sdk.validate import validate_messages, validate_generation_options
from imrabo_ai_sdk.errors import SDKValidationError
from imrabo_ai_sdk.types import Message, GenerationOptions


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
