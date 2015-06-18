# Token bucket

![Token bucket illustration](http://workitmom.com/bloggers/corneredoffice/files/2013/03/bucket-hole.jpg)

A simple rate limiting algorithm. See
[Wikipedia](http://en.wikipedia.org/wiki/Token_bucket) for a more lengthy
discussion of how it works and where it is applicable. In essence, it is a
constant rate limiting with temporal pooling. This allows for bursts of
activity.

It is useful for querying APIs that have rate limits you want to keep under.

## Example

    >>> from tokenbucket import TokenBucket
    >>> tokens = TokenBucket(rate=1.0, maximum=10)
    >>> while have_jobs:
    ...   tokens.take()
    ...   make_request()

## Memcached sharing

Enables sharing across different processes and servers, useful for rate
limiting a shared resource (like a Web API.)

    from tokenbucket import SharedTokenBucket

    tb = SharedTokenBucket(rate=1.0, maximum=5)

    tb.use_memcached_key('my_shared_token_bucket')
    # or
    tb.use_memcached_key('my_shared_token_bucket', client=mc)

