import redis
import time
from redis.exceptions import AuthenticationError


class LeakyBucketRateLimiter:
    def __init__(self, redis_host, redis_port, redis_user, redis_password, ssl=True):
        """
        Initialize Redis client with SASL authentication.
        """
        try:
            self.redis_client = redis.StrictRedis(
                host=redis_host,
                port=redis_port,
                username=redis_user,
                password=redis_password,
                decode_responses=True,
                ssl=ssl, 
                socket_timeout=5
            )
            self.redis_client.ping()
            print("Connected to Redis.")
        except AuthenticationError as e:
            raise Exception(f"Redis authentication failed: {e}")
        except Exception as e:
            raise Exception(f"Redis connection error: {e}")

    def is_rate_limited(self, identifier, capacity, leak_rate):
        """
        Apply the leaky bucket algorithm to limit requests.

        :param identifier: Unique identifier for the client (e.g., IP address)
        :param capacity: Maximum bucket size
        :param leak_rate: Leak rate in requests per second
        :return: True if rate-limited, False otherwise
        """
        key = f"leaky_bucket:{identifier}"
        current_time = int(time.time())

        # Fetch bucket state from Redis
        bucket = self.redis_client.hgetall(key)
        last_checked = int(bucket.get("last_checked", current_time))
        current_size = float(bucket.get("size", 0))

        # Leak the bucket
        elapsed_time = current_time - last_checked
        leaked = elapsed_time * leak_rate
        current_size = max(0, current_size - leaked)

        # Update last checked time and set the TTL
        self.redis_client.hset(key, mapping={"last_checked": current_time, "size": current_size})

        # Set TTL to auto-clear the record
        ttl = int(current_size / leak_rate)
        self.redis_client.expire(key, ttl)

        # Check if the bucket can accommodate the new request
        if current_size < capacity:
            # Accept the request and increase the bucket size
            self.redis_client.hincrbyfloat(key, "size", 1)
            # Update TTL after increment
            ttl = int((current_size + 1) / leak_rate)
            self.redis_client.expire(key, ttl)
            return False  # Not rate-limited
        else:
            return True  # Rate-limited
