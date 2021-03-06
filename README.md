# Token bucket

![Token bucket illustration](http://workitmom.com/bloggers/corneredoffice/files/2013/03/bucket-hole.jpg)

A simple rate limiting algorithm. See
[Wikipedia](http://en.wikipedia.org/wiki/Token_bucket) for a more lengthy
discussion of how it works and where it is applicable. In essence, it is a
constant rate limiting with temporal pooling. This allows for bursts of
activity.

It is useful for querying APIs that have rate limits you want to keep under.

## Example

The principal interaction is done with the `TokenBucket` class. It has two
parameters: **rate**, and **maximum**:

```python
>>> from tokenbucket import TokenBucket
>>> tokens = TokenBucket(rate=1.0, maximum=10)
```

 The rate specifies generation in *tokens per second*, so a rate of ten will
regenerate ten tokens every second. The maximum specifies, well, the maximum
number of tokens before the bucket is full; this limits the regeneration
behavior. It is also the initial number of tokens for new buckets.

To take a token out of the bucket, use the *take* method. It will take one
token or more depending on its argument, and if there aren't enough, it will
wait until there is. A common idiom with is to string this together with a
queue of some kind:

```python
>>> while not queue.empty():
...   tokens.take()
...   do_job()
```

## Memcached sharing

Enables sharing across different processes and servers, useful for rate
limiting a shared resource (like a Web API.) For this we use
`SharedTokenBucket`,

```python
>>> from tokenbucket import SharedTokenBucket
>>> tokens = SharedTokenBucket(rate=1.0, maximum=10)
```

Then sharing options are specified with `use_memcached_key`, which optionally
takes a *client* argument.

```python
>>> tokens.use_memcached_key('my_shared_token_bucket')
```

Other than that, it works just as the basic variant. It is a naive waiting
algorithm and works well with low contetion, and performs quite unevenly in
high contetion situations.
