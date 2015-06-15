import pickle
import time
import tokenbucket
from nose.tools import eq_, ok_

def test_rudimentary():
    tb1 = tokenbucket.TokenBucket(rate=1, maximum=10)
    tb1.take(n=3)
    tb2 = pickle.loads(pickle.dumps(tb1))
    eq_(tb1.tokens, tb2.tokens)
    eq_(tb1.rate, tb2.rate)
    eq_(tb1.maximum, tb2.maximum)
    time.sleep(1)
    tb1.take()
    tb2.take()
    ok_((tb1.tokens - tb2.tokens)**2 < 1e-6)


def test_mc():

    tb1 = tokenbucket.SharedTokenBucket(rate=1, maximum=10)
    tb1.use_memcached_key('test', overwrite=True)

    tb2 = tokenbucket.SharedTokenBucket(rate=1, maximum=10)
    tb2.use_memcached_key('test')

    try:
        tb3 = tokenbucket.SharedTokenBucket(rate=10, maximum=10)
        tb3.use_memcached_key('test')
    except RuntimeError:
        ok_(True)
    else:
        ok_(False)

    eq_(tb2.tokens, tb2.maximum)
    tb1.take(n=tb1.tokens)
    ok_(tb1.tokens**2 < 1e-3)
    tb2.take(0)
    ok_(tb2.tokens**2 < 1e-3)
