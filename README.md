# Introduction
Collie is a fast and simple web framework.

# Features 📈
Collie includes the following features commonly found in many frameworks:
- Fully asynchronous 
- Support for relational databases, model definition, and migrations (using alembic & sqlalchemy)
- Templates (using Jinja2)
- Efficient request routing (with O(n) complexity; future plans include integration of a very fast Radix Router)
- Authentication support (password hashing, time attack protection)
- CORS
- CSRF (not yet)
- Permissions (not yet)
- Middleware chaining (not yet)
- Global settings
- Command manager (manage.py)
- Support for class-based APIs (serialization/deserialization) and asynchronous caching with TTL.
- Generic views (currently limited to functional views)

# Benchmarks 📈
Tests were conducted using PyPy with a single uvicorn worker. You can also conduct your own tests; here are my results:
```bash
$ wrk -t20 -c2000 -d30s http://localhost:8000/login
Running 30s test @ http://localhost:8000/login
  20 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   106.93ms   22.84ms 196.04ms   86.61%
    Req/Sec   670.45    273.86     1.34k    58.45%
  280456 requests in 30.04s, 615.80MB read
  Socket errors: connect 999, read 0, write 0, timeout 0
Requests/sec:   9337.11
Transfer/sec:     20.50MB
```
As you can see, it's blazingly fast even with just a single worker

# Why?
I just got bored.
