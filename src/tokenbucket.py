import time


class TokenBucket():
    "A rate limiting algorithm that allows short bursts of activity"

    def __init__(self, rate, maximum):
        self.rate = rate
        self.maximum = maximum
        self.tokens = maximum
        self._updated = time.time()

    def take(self, n=1):
        "Take n tokens waiting for them to arrive"
        self._regenerate()

        while n > 0:

            if n > self.tokens:
                missing = min(self.maximum, n - self.tokens)
                time.sleep(missing / self.rate)
                self._regenerate()

            take = min(self.tokens, n)
            self.tokens -= take
            n -= take

    def _regenerate(self):
        now = time.time()
        elapsed = now - self._updated
        added = elapsed * self.rate
        self.tokens = min(self.maximum, self.tokens + added)
        self._updated = now

if __name__ == "__main__":
    token_bucket = TokenBucket(maximum=5, rate=1)
    while True:
        token_bucket.take()
        print('Boom! {}'.format(time.time()))
