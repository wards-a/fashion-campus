# About this module

## Getting Started

This module makes use of the [pytest](https://docs.pytest.org/en/7.1.x/contents.html) library.

## How to run

Start the fashion-campus container with docker compose, make sure you are in the fashion-campus directory.

If you make any changes to your code, use `--build`.
```
docker compose up -d
```

Then execute the test,
```
docker exec fashion-campus pytest
```
this command executes all existing tests.
## Other

Please feel free to modify this readme.
