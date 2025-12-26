from ..types import Provider, InternalRequest, GenerateResult, Capabilities


class KernelProvider(Provider):
    def __init__(self):
        self.id = "kernel"

    def capabilities(self) -> Capabilities:
        return Capabilities(streaming=False, tools=False, json=False, max_tokens=None)

    def generate(self, req: InternalRequest) -> GenerateResult:
        raise NotImplementedError("Kernel provider is a stub. Implement later.")

    def stream(self, req: InternalRequest):
        raise NotImplementedError("Kernel provider is a stub. Implement later.")
