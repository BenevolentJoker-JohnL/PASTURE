# Contributing to PASTURE Framework

We love your input! We want to make contributing to PASTURE as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Pull Request Guidelines

- Update the README.md with details of changes to the interface, if appropriate
- Update the documentation with details of any new functionality
- The PR should work for Python 3.8, 3.9, and 3.10
- Write or update tests for any changed functionality

## Development Setup

To set up your local development environment:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pasture.git
cd pasture

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make dev-install
```

## Running Tests

We use pytest for testing:

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov
```

## Code Formatting

We use Black and isort for code formatting:

```bash
# Format code
make format

# Check formatting
make lint
```

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## References

This document was adapted from [GitHub's open-source contribution guidelines](https://github.com/github/docs/blob/main/CONTRIBUTING.md).
