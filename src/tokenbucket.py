"Token bucket rate limiting"

import time
import json


class TokenBucket():
    "A rate limiting algorithm that allows short bursts of activity"

    def __init__(self, rate, maximum):
        self.rate       = rate
        self.maximum    = maximum
        self.tokens     = maximum
        self._updated   = time.time()

    def take(self, n=1):
        "Take n tokens waiting for them to arrive"

        self._update()

        while n > 0:

            if n > self.tokens:
                missing = min(self.maximum, n - self.tokens)
                time.sleep(missing / self.rate)
                self._update()

            take = min(self.tokens, n)
            n   -= take
            self._update(take)

    def _update(self, take=0):
        now     = time.time()
        elapsed = now - self._updated
        added   = elapsed * self.rate - take
        self.tokens   = min(self.maximum, self.tokens + added)
        self._updated = now

    def __getstate__(self):
        return (self.rate, self.maximum, self.tokens, self._updated)

    def __setstate__(self, state):
        (self.rate, self.maximum, self.tokens, self._updated) = state


class SharedTokenBucket(TokenBucket):

    def use_memcached_key(self, key, client=None, overwrite=False):
        """Share the token bucket with others using memcached."""

        if hasattr(self, 'client'):
            raise RuntimeError('token bucket already bound to memcached, '
                               'refusing to rebind')

        if not client:
            import pylibmc
            client = pylibmc.Client(['127.0.0.1'])
            client.behaviors['cas'] = True
            client.behaviors['tcp_nodelay'] = True

        self._mc = client
        self._mc_key = key

        if not self._mc_dump(overwrite=overwrite) and not overwrite:
            # Dump failed and we're not overwriting, so the key might exist.
            self._mc_load()

    def _mc_load(self):

        try:
            (state_serialized, cas) = self._mc.gets(self._mc_key)
            state = tuple(json.loads(state_serialized))
            (rate, maximum, tokens, updated) = state
        except (ValueError, TypeError) as e:
            raise RuntimeError('failed restoring state') from e

        if (rate, maximum) != (self.rate, self.maximum):
            raise RuntimeError('token bucket parameters in memcached mismatch, '
                               'see tb.use_memcached_key(key, overwrite=True)')

        self.__setstate__(state)

        return cas

    def _mc_dump(self, cas=None, overwrite=True):
        state_serialized = json.dumps(self.__getstate__())
        if cas:
            return self._mc.cas(self._mc_key, state_serialized, cas=cas)
        elif overwrite:
            return self._mc.set(self._mc_key, state_serialized)
        else:
            return self._mc.add(self._mc_key, state_serialized)

    def _update(self, *a, **k):
        while True:
            cas = self._mc_load()
            super(SharedTokenBucket, self)._update(*a, **k)
            if self._mc_dump(cas=cas):
                break


if __name__ == "__main__":
    token_bucket = TokenBucket(maximum=5, rate=1)
    while True:
        token_bucket.take()
        print('Boom! {}'.format(time.time()))
