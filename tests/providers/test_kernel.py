import pytest
from imrabo_ai_sdk.providers.kernel import KernelProvider
from imrabo_ai_sdk.types import InternalRequest, Message


def test_kernel_generate_not_implemented():
    p = KernelProvider()
    with pytest.raises(NotImplementedError):
        p.generate(
            InternalRequest(model="m", messages=[Message(role="user", content="hi")])
        )


def test_kernel_stream_not_implemented():
    p = KernelProvider()
    with pytest.raises(NotImplementedError):
        list(
            p.stream(
                InternalRequest(
                    model="m", messages=[Message(role="user", content="hi")]
                )
            )
        )
