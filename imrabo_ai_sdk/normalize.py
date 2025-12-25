from .types import GenerateRequest, InternalRequest, Message
from .validate import validate_messages, validate_generation_options


def normalize_request(request: GenerateRequest) -> InternalRequest:
    validate_messages(request.messages)
    validate_generation_options(request.options)

    # Create an InternalRequest copy and make it immutable via dataclass frozen type
    internal = InternalRequest(
        model=request.model,
        messages=[Message(role=m.role, content=m.content) for m in request.messages],
        tools=request.tools,
        options=request.options,
    )

    return internal
