import random
import string
import time
import uuid

# In-memory store: fine for a single-process dev/demo server.
# For production with multiple workers, move this to Redis or the DB.
_STORE: dict[str, tuple[str, float]] = {}
_TTL_SECONDS = 300


def _cleanup():
    now = time.time()
    expired = [k for k, (_, exp) in _STORE.items() if exp < now]
    for k in expired:
        _STORE.pop(k, None)


def generate_captcha() -> tuple[str, str]:
    """Returns (captcha_id, captcha_text)."""
    _cleanup()
    chars = string.ascii_uppercase.replace("O", "").replace("I", "") + "23456789"
    text = "".join(random.choice(chars) for _ in range(4))
    captcha_id = str(uuid.uuid4())
    _STORE[captcha_id] = (text, time.time() + _TTL_SECONDS)
    return captcha_id, text


def verify_captcha(captcha_id: str, answer: str) -> bool:
    _cleanup()
    entry = _STORE.get(captcha_id)
    if not entry:
        return False
    text, _ = entry
    # one-time use
    _STORE.pop(captcha_id, None)
    return text.strip().upper() == answer.strip().upper()
