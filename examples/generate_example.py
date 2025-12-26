from src.types import GenerateRequest, Message, RuntimeConfig
from src import generate


def main():
    req = GenerateRequest(
        model="gpt-xyz",
        messages=[Message(role="user", content="Hello SDK!")],
        runtime=RuntimeConfig(type="url", endpoint="http://example.com"),
    )

    res = generate(req)
    print("Output:", res.output)


if __name__ == "__main__":
    main()
