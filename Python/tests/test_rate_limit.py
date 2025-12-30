import time
from scanner.core.rate_limit import RateLimiter


def test_rate_limiter_blocks_after_capacity():
    rate = 5
    limiter = RateLimiter(rate)

    start = time.monotonic()
    for _ in range(rate * 2):
        limiter.acquire()
    elapsed = time.monotonic() - start

    assert elapsed >= 0.9
