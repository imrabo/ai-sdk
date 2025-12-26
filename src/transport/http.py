import httpx
from typing import Optional


def post_json(
    url: str,
    headers: Optional[dict] = None,
    json: Optional[dict] = None,
    timeout: Optional[float] = None,
) -> dict:
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(url, headers=headers, json=json)
            resp.raise_for_status()
            return resp.json()
    except httpx.TimeoutException as e:
        raise RuntimeError("timeout") from e
    except httpx.HTTPError as e:
        raise RuntimeError("http error") from e


def post_stream(
    url: str,
    headers: Optional[dict] = None,
    json: Optional[dict] = None,
    timeout: Optional[float] = None,
):
    """A generator that yields bytes chunks from a POST request.

    This keeps the transport layer dumb: it only yields raw bytes chunks. Providers decide how to interpret them.
    """
    try:
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", url, headers=headers, json=json) as resp:
                resp.raise_for_status()
                for chunk in resp.iter_bytes():
                    yield chunk
    except httpx.TimeoutException as e:
        raise RuntimeError("timeout") from e
    except httpx.HTTPError as e:
        raise RuntimeError("http error") from e
