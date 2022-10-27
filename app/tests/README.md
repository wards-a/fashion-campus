# About this module

A test code's location.

Use [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/7.1.x/contents.html) library.

## Getting Started

### Pytest

Use the test_*.py or *_test.py pattern to create your own testing code. See the [documentation](https://docs.pytest.org/en/7.2.x/explanation/goodpractices.html#test-discovery) for more information.

## Testing

### With Pytest

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
