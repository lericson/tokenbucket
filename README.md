# Token bucket

A simple rate limiting algorithm. See
[Wikipedia](http://en.wikipedia.org/wiki/Token_bucket) for a more lengthy
discussion of how it works and where it is applicable. In essence, it is a
constant rate limiting with temporal pooling. This allows for bursts of
activity.
