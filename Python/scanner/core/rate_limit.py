"""
Rate limiting utilities.
"""

from __future__ import annotations

import threading
import time


class RateLimiter:
    """
    Token bucket rate limiter.

    Limits operations to N events per second.
    """

    def __init__(self, rate: int):
        """
        Initialize rate limiter.

        Args:
            rate (int): _description_

        Raises:
            ValueError: _description_
        """
        if rate <= 0:
            raise ValueError("Rate must be greater than zero")

        self.rate = rate
        self.capacity = rate
        self.tokens = rate
        self.lock = threading.Lock()
        self.last_refill = time.monotonic()

    def acquire(self) -> None:
        """
        Acquire permission to perform an operation.
        Blocks until a token is available.
        """

        while True:
            with self.lock:
                self._refill()

                if self.tokens >= 1:
                    self.tokens -= 1
                    return

            time.sleep(0.001)

    def _refill(self) -> None:
        """
        Refill tokens based on elapsed time.
        """

        now = time.monotonic()
        elapsed = now - self.last_refill

        refill_amount = elapsed * self.rate
        if refill_amount >= 1:
            self.tokens = min(
                self.capacity,
                self.tokens + int(refill_amount),
            )
            self.last_refill = now
