"""
=========================================
Retry/Backoff Wrapper (V15)
=========================================
Generic retry-with-exponential-backoff wrapper
for any image provider's generate() call. Any
provider (implemented now or later - Flux,
Gemini, Stability, OpenAI) can use this without
duplicating retry logic.

Retries on transient-looking failures (timeouts,
rate-limits, connection errors) - does NOT retry
on clearly permanent failures (NotImplementedError,
invalid-prompt errors) since retrying those wastes
time and never succeeds.
"""

import time


PERMANENT_FAILURE_TYPES = (
    NotImplementedError,
    ValueError,
)


class RetryExhaustedError(Exception):
    """Raised when all retry attempts fail."""

    def __init__(self, provider_name, attempts, last_error):
        self.provider_name = provider_name
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            f"{provider_name}: all {attempts} attempts failed. "
            f"Last error: {type(last_error).__name__}: {last_error}"
        )


def with_retry(
    func,
    provider_name: str,
    max_attempts: int = 3,
    base_delay_seconds: float = 2.0,
    sleep_fn=time.sleep,
):
    """
    Calls func() with exponential backoff retry: 2s, 4s, 8s
    (for the default base_delay_seconds=2.0).

    func: a zero-argument callable (use a lambda/partial to
          bind actual arguments) that performs the real work.
    provider_name: used in error messages/logging.
    sleep_fn: injectable for testing (avoid real sleeps in tests).

    Raises RetryExhaustedError if every attempt fails.
    Does NOT retry on PERMANENT_FAILURE_TYPES - fails fast instead.
    """
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except PERMANENT_FAILURE_TYPES as e:
            # Not a transient failure - retrying won't help
            raise
        except Exception as e:
            last_error = e
            if attempt < max_attempts:
                delay = base_delay_seconds * (2 ** (attempt - 1))
                sleep_fn(delay)
            continue

    raise RetryExhaustedError(provider_name, max_attempts, last_error)
