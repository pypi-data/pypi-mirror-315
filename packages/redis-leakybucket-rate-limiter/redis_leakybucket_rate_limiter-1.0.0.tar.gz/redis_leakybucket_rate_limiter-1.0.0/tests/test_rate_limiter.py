import pytest
from ratelimiter import LeakyBucketRateLimiter
import time
import os

# Redis configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_USER = os.environ.get("REDIS_USER", None)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

@pytest.fixture(scope="module")
def rate_limiter():
    """
    Fixture to initialize the rate limiter with a Redis client.
    """
    return LeakyBucketRateLimiter(
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        redis_user=REDIS_USER,
        redis_password=REDIS_PASSWORD,
        ssl=False
    )

def test_rate_limiter_allows_requests(rate_limiter):
    """
    Test that the rate limiter allows requests within the limit.
    """
    identifier = "test_user_1"
    capacity = 5
    leak_rate = 1  # 1 request per second

    # Simulate 5 requests
    for _ in range(5):
        assert not rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be allowed"

def test_rate_limiter_blocks_requests(rate_limiter):
    """
    Test that the rate limiter blocks requests exceeding the limit.
    """
    identifier = "test_user_2"
    capacity = 3
    leak_rate = 1  # 1 request per second

    # Simulate 3 allowed requests
    for _ in range(3):
        assert not rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be allowed"

    # Simulate 1 blocked request
    assert rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be blocked"

def test_rate_limiter_leak_rate(rate_limiter):
    """
    Test that the rate limiter allows requests after enough time has passed.
    """
    identifier = "test_user_3"
    capacity = 2
    leak_rate = 1  # 1 request per second

    # Fill the bucket
    for _ in range(2):
        assert not rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be allowed"

    # Wait for the bucket to leak
    import time
    time.sleep(2)

    # Request should be allowed again
    assert not rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be allowed after leak"

def test_rate_limiter_ttl(rate_limiter):
    """
    Test that the Redis key for the rate limiter is deleted after the TTL expires.
    """
    identifier = "test_user_4"
    capacity = 2
    leak_rate = 1  # 1 request per second

    # Fill the bucket to set the key
    for _ in range(2):
        assert not rate_limiter.is_rate_limited(identifier, capacity, leak_rate), "Request should be allowed"

    # Check if the Redis key exists
    redis_client = rate_limiter.redis_client
    key = f"leaky_bucket:{identifier}"
    assert redis_client.exists(key), "Key should exist after requests"

    # Wait for the TTL to expire
    time.sleep(3)  # TTL is based on capacity / leak_rate

    # Verify the key has been deleted
    assert not redis_client.exists(key), "Key should be deleted after TTL expires"
