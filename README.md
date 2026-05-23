# Arceion - Django Microservices Framework

A lightweight Python package providing utilities, decorators, middleware, and ORM integration for building independent microservices with Django.

## Features
- Configurable app initialization
- Authentication and authorization utilities
- Database abstraction layer
- Logging framework
- Middleware components
- Serializers and validators
- RESTful API templates

## Installation

```bash
pip install arceion-zorion
```

## Quick Start

```python
from arceion.zorion.app import API
from arceion.zorion.db import Model, Service
from arceion.zorion.auth import Authorized

# Define models
class User(Model):
    name: str
    email: str

# Define services
class UserService(Service):
    def get_active_users(self):
        return self.getAll(filters={'is_active': True})

# Define APIs
class UserAPI(API):
    userService: UserService = UserService()
    
    @Authorized(required_roles=['admin'])
    def get_users(self, request):
        users = self.userService.getAll()
        return self.response(users)
```

## Documentation

- **[Authorization & Permissions](./arceion/zorion/docs/PERMISSIONS.md)** — Permission system, decorators, best practices
- **[Releasing to PyPI](./RELEASING.md)** — Publishing new versions
- **[GitHub Actions Setup](../.github-actions-setup.md)** — CI/CD configuration

## Development

### Setup

```bash
git clone https://github.com/arceion/arceion-zorion.git
cd arceion-zorion
pip install -e ".[dev]"
```

### Testing

```bash
pytest arceion/zorion/tests/ -v
```

### Publishing

See [RELEASING.md](./RELEASING.md) for:
- Version management
- TestPyPI testing
- Production releases
- Troubleshooting

## License

Proprietary - Arceion
