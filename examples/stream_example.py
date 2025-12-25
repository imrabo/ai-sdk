from imrabo_ai_sdk.types import GenerateRequest, Message, RuntimeConfig
from imrabo_ai_sdk import stream


def main():
    req = GenerateRequest(
        model="gpt-xyz",
        messages=[Message(role="user", content="Stream this")],
        runtime=RuntimeConfig(type="url", endpoint="http://example.com"),
    )

    for chunk in stream(req):
        if chunk.type == "token":
            print(chunk.value, end="", flush=True)
        elif chunk.type == "done":
            print("\n-- DONE --")


if __name__ == "__main__":
    main()
