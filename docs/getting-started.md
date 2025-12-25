# Getting Started

Install from PyPI:

```bash
pip install imrabo-ai-sdk
```

Basic usage:

```python
from imrabo_ai_sdk import generate
from imrabo_ai_sdk.types import GenerateRequest, Message, RuntimeConfig

req = GenerateRequest(
    model='gpt-xyz',
    messages=[Message(role='user', content='Hello')],
    runtime=RuntimeConfig(type='url', endpoint='http://example.com')
)

res = generate(req)
print(res.output)
```

Streaming example:

```python
from imrabo_ai_sdk import stream
for chunk in stream(req):
    if chunk.type == 'token':
        print(chunk.value, end='')
    elif chunk.type == 'done':
        print('\n-- done --')
```

Docs are available under `docs/` in the repository and deployed to GitHub Pages when pushed to `main` (via the docs workflow).
